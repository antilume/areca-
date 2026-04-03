from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import SessionLocal
from app.models import models as db_models
from app.schemas import schemas as api_schemas
from app.tasks.scrapers import scrape_funding_task, scrape_leadership_task, scrape_jobs_task

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[api_schemas.Opportunity])
def list_opportunities(
    source_type: Optional[db_models.SourceType] = None,
    company_name: Optional[str] = None,
    status: Optional[db_models.Status] = None,
    db: Session = Depends(get_db)
):
    query = db.query(db_models.Opportunity)
    if source_type:
        query = query.filter(db_models.Opportunity.source_type == source_type)
    if company_name:
        query = query.filter(db_models.Opportunity.company_name.ilike(f"%{company_name}%"))
    if status:
        query = query.filter(db_models.Opportunity.status == status)

    return query.order_by(db_models.Opportunity.created_at.desc()).all()

@router.get("/{opportunity_id}", response_model=api_schemas.Opportunity)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opp = db.query(db_models.Opportunity).filter(db_models.Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp

@router.patch("/{opportunity_id}", response_model=api_schemas.Opportunity)
def update_opportunity(
    opportunity_id: int,
    opp_update: api_schemas.OpportunityUpdate,
    db: Session = Depends(get_db)
):
    opp = db.query(db_models.Opportunity).filter(db_models.Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    if opp_update.status is not None:
        opp.status = opp_update.status

    db.commit()
    db.refresh(opp)
    return opp

@router.post("/trigger-scan")
def trigger_scan(scan_type: str):
    if scan_type == "funding":
        task = scrape_funding_task.delay()
        return {"task_id": task.id, "status": "Funding scan triggered"}
    elif scan_type == "leadership":
        task = scrape_leadership_task.delay()
        return {"task_id": task.id, "status": "Leadership scan triggered"}
    elif scan_type == "jobs":
        task = scrape_jobs_task.delay()
        return {"task_id": task.id, "status": "Jobs scrape triggered"}
    else:
        raise HTTPException(status_code=400, detail="Invalid scan type")
