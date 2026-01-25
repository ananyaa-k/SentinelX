from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def start_scheduler(job_func, hours=24):
    """Starts the background scheduler."""
    if not scheduler.running:
        scheduler.add_job(
            job_func,
            trigger=IntervalTrigger(hours=hours),
            id='threat_feed_sync',
            name='Sync Threat Intelligence Feeds',
            replace_existing=True
        )
        scheduler.start()
        logger.info(f"Scheduler started with {hours}h interval.")
