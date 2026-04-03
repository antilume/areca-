import hashlib
import json
import re
from sqlalchemy.orm import Session
from app.models.models import RawSignal, SourceType, Company, Opportunity, OpportunityType, Status
from datetime import datetime

class Processor:
    def __init__(self, db: Session):
        self.db = db

    def generate_checksum(self, data: dict) -> str:
        s = json.dumps(data, sort_keys=True)
        return hashlib.md5(s.encode()).hexdigest()

    def save_raw_signal(self, data: dict, source_type: SourceType, source_name: str):
        checksum = self.generate_checksum(data)
        existing = self.db.query(RawSignal).filter(RawSignal.checksum == checksum).first()
        if existing:
            return None

        signal = RawSignal(
            source_type=source_type,
            source_name=source_name,
            payload=json.dumps(data),
            checksum=checksum
        )
        self.db.add(signal)
        self.db.commit()
        return signal

    def normalize_company_name(self, name: str) -> str:
        if not name: return "Unknown"
        # Remove common startup suffixes and clean special characters
        name = name.strip().lower()
        name = re.sub(r' (inc|inc\.|pvt\. ltd\.|private limited|ltd\.|ltd|corporation|corp\.|limited)$', '', name)
        # Clean extra spaces and capitalize
        name = " ".join(name.split())
        return name.title()

    def get_or_create_company(self, name: str) -> Company:
        normalized_name = self.normalize_company_name(name)
        company = self.db.query(Company).filter(Company.name == normalized_name).first()
        if not company:
            company = Company(name=normalized_name)
            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)
        return company

    def dedup_opportunity(self, company_id: int, source_type: SourceType, role_title: str = None) -> bool:
        query = self.db.query(Opportunity).filter(
            Opportunity.company_id == company_id,
            Opportunity.source_type == source_type
        )
        if role_title:
            query = query.filter(Opportunity.role_title == role_title)

        # Check if an opportunity was created within the last 30 days
        # (Very simple time-based dedup for MVP)
        # For funding/leadership, usually once per round/change is enough
        return query.count() > 0

    def process_funding_signal(self, signal_data: dict):
        title = signal_data.get('title', '')
        company_name = self.extract_company_from_title(title)
        company = self.get_or_create_company(company_name)

        if self.dedup_opportunity(company.id, SourceType.FUNDING):
            return

        opportunity = Opportunity(
            company_id=company.id,
            company_name=company.name,
            source_type=SourceType.FUNDING,
            source_name=signal_data.get('source'),
            source_url=signal_data.get('url'),
            opportunity_type=OpportunityType.EXPANSION,
            signal_summary=title,
            raw_context=json.dumps(signal_data),
            hiring_intent_score=self.score_funding(title),
            status=Status.NEW
        )
        self.db.add(opportunity)
        self.db.commit()

    def process_leadership_signal(self, signal_data: dict):
        title = signal_data.get('title', '')
        company_name = self.extract_company_from_title(title)
        company = self.get_or_create_company(company_name)

        role, dept = self.infer_role_and_dept(title)
        if self.dedup_opportunity(company.id, SourceType.LEADERSHIP_CHANGE, role):
            return

        opportunity = Opportunity(
            company_id=company.id,
            company_name=company.name,
            source_type=SourceType.LEADERSHIP_CHANGE,
            source_name=signal_data.get('source'),
            source_url=signal_data.get('url'),
            role_title=role,
            department=dept,
            opportunity_type=OpportunityType.RESTRUCTURING,
            signal_summary=title,
            raw_context=json.dumps(signal_data),
            hiring_intent_score=self.score_leadership(title),
            status=Status.NEW
        )
        self.db.add(opportunity)
        self.db.commit()

    def process_job_signal(self, signal_data: dict):
        title = signal_data.get('title', '')
        company_name = signal_data.get('company', 'See post')
        company = self.get_or_create_company(company_name)

        if self.dedup_opportunity(company.id, SourceType.STARTUP_JOB_POST, title):
            return

        opportunity = Opportunity(
            company_id=company.id,
            company_name=company.name,
            source_type=SourceType.STARTUP_JOB_POST,
            source_name=signal_data.get('source'),
            source_url=signal_data.get('url'),
            role_title=title,
            opportunity_type=OpportunityType.ACTIVE_HIRING,
            signal_summary=f"New job posted: {title}",
            raw_context=json.dumps(signal_data),
            hiring_intent_score=50.0,
            status=Status.NEW
        )
        self.db.add(opportunity)
        self.db.commit()

    def extract_company_from_title(self, title: str) -> str:
        # Better extraction for Entrackr headlines which often start with "Company Raises..."
        # or "Company appoints..."
        match = re.match(r'^([\w\s]+) (raises|appoints|hires|names|secures|gets)', title, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        parts = title.split(' ')
        return parts[0] if parts else "Unknown"

    def infer_role_and_dept(self, title: str):
        title_lower = title.lower()
        role, dept = None, None
        if "cto" in title_lower or "vp engineering" in title_lower or "head of engineering" in title_lower:
            role = "CTO / VP Engineering"
            dept = "Engineering"
        elif "ceo" in title_lower or "founder" in title_lower:
            role = "CEO / Founder"
            dept = "Leadership"
        elif "product" in title_lower:
            role = "Head of Product"
            dept = "Product"
        elif "marketing" in title_lower or "cmo" in title_lower:
            role = "CMO / Head of Marketing"
            dept = "Marketing"
        return role, dept

    def score_funding(self, title: str) -> float:
        score = 60.0
        title_lower = title.lower()
        if "series a" in title_lower: score += 20
        elif "series b" in title_lower: score += 25
        elif "series c" in title_lower: score += 30
        elif "seed" in title_lower: score += 10
        return min(score, 100.0)

    def score_leadership(self, title: str) -> float:
        score = 50.0
        title_lower = title.lower()
        if "cto" in title_lower or "engineering" in title_lower: score += 20
        if "product" in title_lower: score += 15
        if "ceo" in title_lower: score += 10
        return min(score, 100.0)
