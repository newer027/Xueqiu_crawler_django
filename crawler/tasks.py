from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from .utils import save_latest_change
from .models import Portfolio

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/15',hour='9,10,11,13,14',day_of_week='1,2,3,4,5')),
    name="task_save_latest_protfilio_change",
    ignore_result=True
)


def task_save_latest_protfilio_change():
    """
    Saves latest image from Flickr
    """
    for url in Portfolio.objects.all():
        save_latest_change(url.slug)
    logger.info("Saved change from Xueqiu")
