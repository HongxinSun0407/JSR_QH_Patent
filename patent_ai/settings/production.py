import datetime
import os
# 线上测试环境
from openai import OpenAI
from .base import *

DEBUG = False

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['http://39.98.211.187:8990']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'patent_chat_test',
        'USER': 'root',
        'PASSWORD': 'patent_chat_passwd',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'TIME_ZONE': 'Asia/Shanghai',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET time_zone = '+08:00';",
            'connect_timeout': 60,
            'read_timeout': 60,
            'write_timeout': 60,
        }
    }
}
API_KEY = "sk-VGQ3ThuDE16RwerxImfXQgA6afQgZBav968G2PKiIElhMlIy"
MODEL = "moonshot-v1-128k"
# kimi
KIMI_CLIENT = OpenAI(
    api_key=API_KEY,
    base_url="https://api.moonshot.cn/v1",
)
# 天工
APP_KEY = "e79c69c28d1a1a814f737253af5fd7f1"
APP_SECRET = "1316057e6271e1c05c96dd22ee345b37b507339e8c51f7c9"
LIBREOFFICE = "libreoffice7.6"

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/15'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/15'