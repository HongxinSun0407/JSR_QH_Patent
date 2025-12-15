from django.contrib.auth.models import User, AbstractUser
from django.db import models
from rest_framework import serializers


class UserModel(AbstractUser):
    department = models.CharField(max_length=255, null=True, default="",verbose_name="用户部门")
    all_analysis_count = models.IntegerField(default=5, verbose_name="允许解析的数量")
    class Meta:
        db_table = 'auto_user'
        verbose_name = "用户"


def validate_positive(value):
    if value <= 0:
        raise serializers.ValidationError('必须是正数')


