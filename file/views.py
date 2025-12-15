import hashlib
import json
import os
import uuid
from datetime import datetime

from django.conf import settings
from django.core.serializers import serialize
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from pathlib import Path

from patent_ai.exceptions import logger
from rest_framework.mixins import UpdateModelMixin

from analysis.models import ChatSessionModel
from file.models import FileContentModel, FileModel, FileSerializer
from patent_ai.settings.base import KIMI_TIMEOUT

# Create your views here.
class FileListView(View):
    def post(self, request, session_id):
        file = request.FILES.get('file')
        md5 = calculate_md5(file)
        file_model = FileModel.objects.get(md5=md5)
        if file_model is None:
            return JsonResponse(FileSerializer(file_model).data)
        if 'file' not in request.FILES:
            return 'No file part'
        # file = request.files['file']
        file_name = file.name
        # 分离文件名和后缀
        name, ext = os.path.splitext(file_name)
        # 将后缀改为小写
        new_ext = ext.lower()
        # 返回修改后的文件名
        new_file_name = name + new_ext

        file_path = get_file_prefix() + f"/{new_file_name}"
        os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return JsonResponse(upload_file_service(session_id, file_path))

@transaction.atomic
def upload_file_service(session_id: int, file_path):
    """
    上传文件
    :return:
    """
    md5 = get_file_md5(file_path)
    file_model = FileModel.objects.filter(md5=md5, md5__isnull=False).first()
    if file_model is not None:
        return FileSerializer(file_model).data
    # 分离文件名和后缀
    name, ext = os.path.splitext(os.path.basename(file_path))
    # 将后缀改为小写
    new_ext = ext.lower()
    # 返回修改后的文件名
    new_file_path = file_path
    # os.rename(file_path, new_file_path)
    try:
        file_object = settings.KIMI_CLIENT.files.create(file=Path(file_path), purpose="file-extract", timeout=KIMI_TIMEOUT)
    except Exception as e:
        logger.error(new_file_path,e)
        raise e
    try:

        session_model = ChatSessionModel.objects.get(id=session_id)
        file_model = FileModel(id=file_object.id, name=file_object.filename, session_id=session_model,
                               status=file_object.status, file_path=new_file_path, md5=get_file_md5(new_file_path))
        content = settings.KIMI_CLIENT.files.content(file_id=file_object.id).text
        content = json.dumps(json.loads(content),ensure_ascii=False).encode('utf-8', 'replace').decode('utf-8')
        file_content_model = FileContentModel(file_id=file_model,
                                              content=content)
        file_model.save()
        file_content_model.save()
        FileSerializer(file_model)
        return FileSerializer(file_model).data
    finally:
        settings.KIMI_CLIENT.files.delete(file_id=file_object.id)

def get_file_prefix(dir=None):
        current_datetime = datetime.now()
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day
        hour = current_datetime.hour
        if dir is None:
            result = f"upload/{year}/{month}/{day}/{hour}/{uuid.uuid4()}/"
        else:
            result = f"upload/{year}/{month}/{day}/{hour}/{dir}/{uuid.uuid4()}/"
        os.makedirs(result, exist_ok=True)
        return result
def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        # 分块读取文件，避免内存占用过大
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def calculate_md5(file):
    hash_md5 = hashlib.md5()
    for chunk in file.chunks():
        hash_md5.update(chunk)
    return hash_md5.hexdigest()