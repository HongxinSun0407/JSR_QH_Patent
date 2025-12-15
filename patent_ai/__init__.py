# 这将确保应用在Django启动时就加载Celery
from .celery import app as celery_app

__all__ = ('celery_app',)