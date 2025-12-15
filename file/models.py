import json

from django.db import models
from django.utils.timezone import now

from analysis.models import ChatSessionModel
from rest_framework import serializers

# Create your models here.
class FileModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True, verbose_name="主键")
    name = models.CharField(max_length=255,verbose_name="文件名称")
    session_id = models.ForeignKey(ChatSessionModel, on_delete=models.CASCADE,db_column="session_id", verbose_name="session_id")
    status = models.CharField(max_length=255, verbose_name="状态")
    file_path = models.CharField(max_length=255, verbose_name="文件地址")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    md5 = models.CharField(max_length=255, null=True, unique=True,verbose_name="md5")
    class Meta:
        db_table = 'file'
        verbose_name = "文件"
    def file_content(self):
        return json.loads(FileContentModel.objects.get(file_id=self.id).content)['content']
    file_content.short_description = '文件内容'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = ['id', 'name', 'session_id', 'status', 'create_time']

class FileContentModel(models.Model):
    id = models.AutoField(primary_key=True)
    file_id = models.ForeignKey(FileModel, on_delete=models.CASCADE, db_column="file_id", verbose_name="文件id")
    content = models.TextField(verbose_name="解析到的文件的内容")
    class Meta:
        db_table = 'file_content'
        verbose_name = "文件内容"
class FileContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileContentModel
        fields = ['id', 'file_id', 'content']