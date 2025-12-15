from django.contrib import admin
from django.contrib.admin import ModelAdmin

from analysis.models import *


class ProblemLabelAdmin(ModelAdmin):
    list_display = ('seq', 'name', 'create_time')


class ChatContentAdmin(ModelAdmin):
    list_display = ('role', 'create_time')


class ZipAnalysisAdmin(ModelAdmin):
    list_display = ('name', 'status', 'total', 'create_time', 'update_time')


class ResultExportAdmin(ModelAdmin):
    list_display = ('apply_code', 'patent_name', 'department', 'create_time', 'update_time')


class ZipAnalysisResultAdmin(ModelAdmin):
    list_display = ('name', 'status', 'desc', 'create_time')


# Register your models here.
admin.site.register(ProblemLabelModel, ProblemLabelAdmin)
admin.site.register(ChatContentModel, ChatContentAdmin)
admin.site.register(ZipAnalysisModel, ZipAnalysisAdmin)
admin.site.register(ResultExportModel, ResultExportAdmin)
admin.site.register(ZipAnalysisResultModel, ZipAnalysisResultAdmin)
