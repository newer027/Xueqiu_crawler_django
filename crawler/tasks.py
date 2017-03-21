from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from crawler.utils import save_latest_change
from crawler.models import Portfolio

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/3')),
    name="task_save_latest_protfilio_change",
    ignore_result=True
)
def task_save_latest_protfilio_change():
    """
    Saves latest image from Flickr
    """
    for url in Portfolio.objects.all():
        save_latest_change(url.title)
    logger.info("Saved change from Xueqiu")
