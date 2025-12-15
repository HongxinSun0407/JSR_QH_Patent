from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Permission, Group
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy

from analysis.models import ZipAnalysisResultModel
from user.models import UserModel
from django.contrib import admin

class ZipAnalysisResultLine(admin.TabularInline):
    model = ZipAnalysisResultModel
    extra = 0
    readonly_fields = ("create_time",)
    fields = ['create_time',]
class UserProfileAdmin(UserAdmin):
    # 重建对象详细表排列结构
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),

        (gettext_lazy('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',
                                                  'groups', 'user_permissions')}),

        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (gettext_lazy('Personal info'), {'fields': ('all_analysis_count', 'department')})
    )
    inlines = [ZipAnalysisResultLine]

class GroupAdminForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple('Users', is_stacked=False)
    )

    permissions = forms.ModelMultipleChoiceField(
        queryset=Group._meta.get_field('permissions').related_model.objects.all(),
        required=False,
        widget=widgets.FilteredSelectMultiple('Permissions', is_stacked=False)
    )

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()
            self.fields['permissions'].initial = self.instance.permissions.all()

    def save(self, commit=True):
        group = super().save(commit=False)
        if commit:
            group.save()
        if group.pk:
            group.user_set.set(self.cleaned_data['users'])
            group.permissions.set(self.cleaned_data['permissions'])
            self.save_m2m()
        return group
class CustomGroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ['name']
    search_fields = ['name']

    # 定义详情页面要显示的字段集
    fieldsets = (
        (None, {'fields': ('name', 'permissions', 'users')}),
    )

    # 设置过滤和搜索功能
    filter_horizontal = ('permissions',)
admin.site.register(UserModel, UserProfileAdmin)
admin.site.register(Permission)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
