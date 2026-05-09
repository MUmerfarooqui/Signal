from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

celery = Celery(
    "signal",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["workers.embed", "workers.brief"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        # Every Monday at 8am UTC — briefs are generated per-org by a separate fan-out task
        "weekly-briefs": {
            "task": "workers.brief.dispatch_all_orgs",
            "schedule": crontab(hour=8, minute=0, day_of_week=1),
        },
    },
)
