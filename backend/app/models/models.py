from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class SourceType(enum.Enum):
    FUNDING = "funding"
    LEADERSHIP_CHANGE = "leadership_change"
    STARTUP_JOB_POST = "startup_job_post"

class OpportunityType(enum.Enum):
    EXPANSION = "expansion"
    RESTRUCTURING = "restructuring"
    ACTIVE_HIRING = "active_hiring"

class Status(enum.Enum):
    NEW = "new"
    REVIEWING = "reviewing"
    CONTACTED = "contacted"
    IGNORED = "ignored"

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    website = Column(String, nullable=True)
    location = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    opportunities = relationship("Opportunity", back_populates="company")
    decision_makers = relationship("DecisionMaker", back_populates="company")

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company_name = Column(String)
    source_type = Column(Enum(SourceType))
    source_name = Column(String)
    source_url = Column(String)
    role_title = Column(String, nullable=True)
    department = Column(String, nullable=True)
    opportunity_type = Column(Enum(OpportunityType))
    signal_summary = Column(Text)
    raw_context = Column(Text)
    hiring_intent_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    freshness_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    decision_maker_id = Column(Integer, ForeignKey("decision_makers.id"), nullable=True)
    status = Column(Enum(Status), default=Status.NEW)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="opportunities")
    decision_maker = relationship("DecisionMaker")

class DecisionMaker(Base):
    __tablename__ = "decision_makers"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    full_name = Column(String)
    title = Column(String)
    linkedin_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
    confidence_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="decision_makers")

class RawSignal(Base):
    __tablename__ = "raw_signals"

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(Enum(SourceType))
    source_name = Column(String)
    payload = Column(Text)  # JSON stored as text
    checksum = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
