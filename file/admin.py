from django.contrib import admin

from file.models import *

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'create_time','md5')
    readonly_fields = ['file_content']
# Register your models here.
admin.site.register(FileModel,FileAdmin)
