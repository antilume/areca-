import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models.models import DecisionMaker, Company, Opportunity
import cloudscraper
import random
import re

class DecisionMakerService:
    def __init__(self, db: Session):
        self.db = db
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
        )
        self.fake_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
        ]

    def get_ua(self):
        return {"User-Agent": random.choice(self.fake_agents)}

    def find_decision_maker(self, company: Company):
        if not company.website:
            company.website = self.guess_website(company.name)
            self.db.commit()

        # Look for existing DM
        existing = self.db.query(DecisionMaker).filter(DecisionMaker.company_id == company.id).first()
        if existing:
            return existing

        # Slightly better "discovery" logic
        # In a real MVP, we'd search: site:linkedin.com/in "Founder" "Company Name"
        # We simulate the most likely candidates for outreach
        dm = self.create_potential_dm(company)
        return dm

    def guess_website(self, company_name: str) -> str:
        clean_name = company_name.lower().replace(" ", "")
        return f"https://{clean_name}.com"

    def create_potential_dm(self, company: Company) -> DecisionMaker:
        # For India startups, Founders are the best targets for agency/recruiter outreach
        dm = DecisionMaker(
            company_id=company.id,
            full_name=f"Founder / CEO", # Generic until enriched
            title="Founder / CEO",
            confidence_score=40.0,
            linkedin_url=f"https://www.linkedin.com/search/results/people/?keywords={company.name}%20Founder"
        )
        self.db.add(dm)
        self.db.commit()
        self.db.refresh(dm)
        return dm

    def attach_dm_to_opportunity(self, opportunity: Opportunity):
        company = self.db.query(Company).filter(Company.id == opportunity.company_id).first()
        if company:
            dm = self.find_decision_maker(company)
            if dm:
                opportunity.decision_maker_id = dm.id
                self.db.commit()
