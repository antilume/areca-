from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models.models import SourceType, OpportunityType, Status

class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DecisionMakerBase(BaseModel):
    full_name: str
    title: str
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    confidence_score: float

class DecisionMaker(DecisionMakerBase):
    id: int
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class OpportunityBase(BaseModel):
    company_id: int
    company_name: str
    source_type: SourceType
    source_name: str
    source_url: str
    role_title: Optional[str] = None
    department: Optional[str] = None
    opportunity_type: OpportunityType
    signal_summary: str
    raw_context: str
    hiring_intent_score: float
    quality_score: float = 0.0
    freshness_score: float = 0.0
    final_score: float = 0.0
    status: Status

class OpportunityUpdate(BaseModel):
    status: Optional[Status] = None

class Opportunity(OpportunityBase):
    id: int
    decision_maker_id: Optional[int] = None
    decision_maker: Optional[DecisionMaker] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
