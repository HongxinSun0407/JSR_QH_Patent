from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
# 设置默认的Django settings模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patent_ai.settings.online')

app = Celery('patent_ai')

# 从Django的settings.py中加载配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现异步任务
app.autodiscover_tasks()