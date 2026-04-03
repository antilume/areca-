from app.tasks import celery_app
from app.services.scrapers import EntrackrScraper, WellfoundScraper, InternshalaScraper
from app.services.processor import Processor
from app.services.decision_maker import DecisionMakerService
from app.core.database import SessionLocal
from app.models.models import SourceType, Opportunity

@celery_app.task
def scrape_funding_task():
    db = SessionLocal()
    scraper = EntrackrScraper()
    processor = Processor(db)
    dm_service = DecisionMakerService(db)

    signals = scraper.scrape_funding()
    for signal in signals:
        raw_signal = processor.save_raw_signal(signal, SourceType.FUNDING, "entrackr")
        if raw_signal:
            processor.process_funding_signal(signal)
            # Find and attach DM
            latest_opp = db.query(Opportunity).filter(
                Opportunity.source_url == signal.get('url')
            ).first()
            if latest_opp:
                dm_service.attach_dm_to_opportunity(latest_opp)

    db.close()
    return f"Funding scan complete, processed {len(signals)} items."

@celery_app.task
def scrape_leadership_task():
    db = SessionLocal()
    scraper = EntrackrScraper()
    processor = Processor(db)
    dm_service = DecisionMakerService(db)

    signals = scraper.scrape_leadership()
    for signal in signals:
        raw_signal = processor.save_raw_signal(signal, SourceType.LEADERSHIP_CHANGE, "entrackr")
        if raw_signal:
            processor.process_leadership_signal(signal)
            latest_opp = db.query(Opportunity).filter(
                Opportunity.source_url == signal.get('url')
            ).first()
            if latest_opp:
                dm_service.attach_dm_to_opportunity(latest_opp)

    db.close()
    return f"Leadership scan complete, processed {len(signals)} items."

@celery_app.task
def scrape_jobs_task():
    db = SessionLocal()
    processor = Processor(db)
    dm_service = DecisionMakerService(db)

    # Wellfound
    wellfound = WellfoundScraper()
    wf_jobs = wellfound.scrape_jobs()
    for job in wf_jobs:
        raw_signal = processor.save_raw_signal(job, SourceType.STARTUP_JOB_POST, "wellfound")
        if raw_signal:
            processor.process_job_signal(job)
            latest_opp = db.query(Opportunity).filter(
                Opportunity.source_url == job.get('url')
            ).first()
            if latest_opp:
                dm_service.attach_dm_to_opportunity(latest_opp)

    # Internshala
    internshala = InternshalaScraper()
    is_jobs = internshala.scrape_internships()
    for job in is_jobs:
        raw_signal = processor.save_raw_signal(job, SourceType.STARTUP_JOB_POST, "internshala")
        if raw_signal:
            processor.process_job_signal(job)
            latest_opp = db.query(Opportunity).filter(
                Opportunity.source_url == job.get('url')
            ).first()
            if latest_opp:
                dm_service.attach_dm_to_opportunity(latest_opp)

    db.close()
    return f"Jobs scrape complete, processed {len(wf_jobs) + len(is_jobs)} items."
