import json
import traceback

import logging
from django.http import Http404
from openai import APIStatusError
from rest_framework.response import Response
logger = logging.getLogger('patent_ai')

def handle_exceptions(err, context):
        traceback.print_exc()

        try:
            error_code = err.status_code
        except Exception:
            error_code = 500
        try:
            message = err.default_detail
        except Exception:
            message = '未知错误'
        if isinstance(err, Http404):
            error_code = 404
            message = "没有数据"
        if isinstance(err, APIStatusError):
            error_code = err.code
            # 如果 error 字段存在，再从中提取 body 字段的值
            if err.status_code == 429:
                message = "请求触发了账户速率限制，请等待指定时间后重试"
            if err.status_code == 400:
                message = "请求内容拒绝"
            if err.status_code == 401:
                message = "认证失败"
            if err.status_code == 403:
                message = "账户异常，请检查您的账户余额"
            if err.status_code == 500:
                message = "文件解析出错"
            else:
                message = "文件解析出错"
        logger.error("错误%s", err, exc_info=True)
        return Response(message, status=error_code)
