from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    beat_schedule={
        "scrape_funding_periodic": {
            "task": "app.tasks.scrapers.scrape_funding_task",
            "schedule": 21600.0,  # 6 hours
        },
        "scrape_leadership_periodic": {
            "task": "app.tasks.scrapers.scrape_leadership_task",
            "schedule": 21600.0,  # 6 hours
        },
        "scrape_jobs_periodic": {
            "task": "app.tasks.scrapers.scrape_jobs_task",
            "schedule": 10800.0,  # 3 hours
        },
    },
)

# Import tasks to ensure they are registered
import app.tasks.scrapers
