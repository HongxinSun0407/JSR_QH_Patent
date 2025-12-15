from django.db import models
from django.utils.timezone import now
from rest_framework import serializers

from user.models import UserModel


# Create your models here.
class ChatSessionModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user_id = models.ForeignKey(UserModel, on_delete=models.SET(1), db_column="user_id", verbose_name='用户id',default=1)
    class Meta:
        db_table = 'chat_session'
        verbose_name = 'SessionModel'


class ProblemLabelModel(models.Model):
    id = models.AutoField(primary_key=True)
    seq = models.IntegerField(verbose_name='问题序号')
    name = models.TextField(verbose_name='问题名称')
    kimi_content = models.TextField(null=True, blank=True,verbose_name='kimi问题')
    tiangong_content = models.TextField(null=True, blank=True, verbose_name='天工问题')
    # 请求天工的类型
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    tiangong_type = models.IntegerField(null=True,verbose_name='请求天工的类型 1简单 2 增强 3 研究 4 作图 ')
    tiangong_content1 = models.TextField(null=True, blank=True, verbose_name='天工的问题')
    tiangong_content2 = models.TextField(null=True, blank=True,verbose_name='天工的问题')
    kimi_content1 = models.TextField(null=True, blank=True,verbose_name='kimi的问题')
    kimi_content2 = models.TextField(null=True, blank=True,verbose_name='kimi的问题')

    class Meta:
        db_table = 'problem_label'
        verbose_name = '问题Model'


class ChatContentModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    role = models.CharField(max_length=255,verbose_name='角色')
    file_json = models.JSONField(null=True,verbose_name='文件的json')
    content = models.JSONField(null=True,verbose_name='请求kimi的回答')
    problem_label_id = models.ForeignKey(ProblemLabelModel, on_delete=models.CASCADE, db_column="problem_label_id", verbose_name='问题id')
    session_id = models.ForeignKey(ChatSessionModel, on_delete=models.CASCADE, db_column="session_id")
    group_id = models.CharField(max_length=255,verbose_name='问答组id')
    tiangong_answer = models.TextField(null=True,verbose_name='请求天工的答案')
    request_tiangong = models.JSONField(null=True,verbose_name='请求天工的json数据')
    request_kimi = models.JSONField(null=True,verbose_name='请求kimi的json数据')
    # 天工的参考链接
    ref_link = models.JSONField(null=True,verbose_name='天工问答检索到的链接列表')
    user_id = models.ForeignKey(UserModel, on_delete=models.SET(1), db_column="user_id", verbose_name='用户id',default=1)
    class Meta:
        db_table = 'chat_content'
        verbose_name = '问答Model'


class ZipAnalysisModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,verbose_name='压缩包名称')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    status = models.CharField(max_length=255,verbose_name='处理状态')
    total = models.IntegerField(verbose_name='压缩包中的文件个数')
    user_id = models.ForeignKey(UserModel, on_delete=models.SET(1), db_column="user_id", verbose_name='用户id', default=1)
    docx_file = models.FileField(upload_to="upload/zip_result/%Y/%m/%d/%H/%M", verbose_name="生成的docx压缩包文件",
                                    db_comment="生成的docx文件", null=True)
    pdf_file = models.FileField(upload_to="upload/zip_result/%Y/%m/%d/%H/%M", verbose_name="生成的pdf压缩包文件",
                                    db_comment="生成的pdf文件", null=True)
    class Meta:
        db_table = 'zip_analysis'
        verbose_name = '压缩包Model'

    def __str__(self):
        return self.name

class ZipAnalysisResultModel(models.Model):
    id = models.AutoField(primary_key=True)
    zip_id = models.ForeignKey(ZipAnalysisModel, on_delete=models.CASCADE, db_column="zip_id",verbose_name='压缩包id')
    session_id = models.ForeignKey(ChatSessionModel, on_delete=models.CASCADE, db_column="session_id",verbose_name='session_id')
    name = models.CharField(max_length=255,verbose_name='文件名称')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    status = models.CharField(max_length=255,verbose_name='专利状态')
    desc = models.CharField(max_length=255, null=True,verbose_name='描述信息')
    patent_info = models.JSONField(verbose_name='专利基础信息',null=True)
    file_id = models.CharField(max_length=255,verbose_name='文件id')
    # 生成状态 0失败 1成功
    generate_status = models.IntegerField(null=True, verbose_name='生成docx状态')
    user_id = models.ForeignKey(UserModel, on_delete=models.SET(1), db_column="user_id", verbose_name='用户id',default=1)
    rest_count = models.IntegerField(default=0, verbose_name='重新解析的次数')
    docx_file = models.FileField(upload_to="upload/zip_result/%Y/%m/%d/%H/%M", verbose_name="生成的docx文件",
                                    db_comment="生成的docx文件", null=True)
    pdf_file = models.FileField(upload_to="upload/zip_result/%Y/%m/%d/%H/%M", verbose_name="生成的pdf文件",
                                    db_comment="生成的pdf文件", null=True)
    class Meta:
        db_table = 'zip_analysis_result'
        permissions = [
            ("upload_zip", "上传压缩包进行解析"),
            ("reanalysis_file", "重新解析压缩包中的文件"),
            ("down_word", "将压缩包中解析成功的文件下载"),
            ("batch_down_docx", "将压缩包中的文件批量下载"),
        ]
        verbose_name = '压缩包中解析的文件'

    def __str__(self):
        return self.name


class ResultExportModel(models.Model):
    id = models.AutoField(primary_key=True)
    apply_code = models.CharField(max_length=255)
    inventor = models.CharField(max_length=255, verbose_name='发明人', default="")
    legal_status = models.CharField(max_length=255, verbose_name='法律状态', default="")
    maintenance_period = models.CharField(max_length=255, verbose_name='维持年限', default="")
    neic = models.CharField(max_length=255, verbose_name='国民经济行业分类', default="")
    new_classification = models.CharField(max_length=255, verbose_name='战新分类', default="")
    ipc = models.CharField(max_length=255, verbose_name='ipc', default="")
    technical_topic_class = models.CharField(max_length=255, verbose_name='技术主题分类', default="")
    application_field_class = models.CharField(max_length=255, verbose_name='应用领域分类', default="")
    neic_num = models.CharField(max_length=255, verbose_name='国民经济行业分类号', default="")
    ai_score = models.CharField(max_length=255, verbose_name='ai分数', default="")
    problem_solved = models.CharField(max_length=255, verbose_name='所解决的问题', default="")
    patent_name = models.CharField(max_length=255, verbose_name='专利名称')
    com_patent_name = models.CharField(max_length=255, verbose_name='组合专利名称', null=True, blank=True )
    com_patent_info = models.CharField(max_length=255, verbose_name='组合专利信息', null=True, blank=True )
    com_patent_desc = models.CharField(max_length=255, verbose_name='组合专利描述', null=True, blank=True)
    is_financially_supported = models.CharField(max_length=255, null=True,
                                                verbose_name='是否属于财政资助科研项目形成专利', blank=True)
    level_first = models.CharField(max_length=255, null=True, verbose_name='一级实施状态', blank=True)
    level_second = models.CharField(max_length=255, null=True, verbose_name='二级状态描述', blank=True)
    money = models.CharField(max_length=255, null=True, verbose_name='金额', blank=True)
    remark = models.TextField(max_length=255, null=True, verbose_name='备注', blank=True)
    conversion_first = models.CharField(max_length=255, null=True, verbose_name='转化意愿（一级）', blank=True)
    conversion_second = models.CharField(max_length=255, null=True, verbose_name='转化意愿（二级）', blank=True)
    stand_money = models.CharField(max_length=255, null=True, verbose_name='费用标准', blank=True)
    cooperative_enterprises = models.TextField(max_length=255, verbose_name='合作企业', null=True,  blank=True)
    cooperative_city = models.TextField(max_length=255, verbose_name='合作企业城市', null=True,  blank=True)
    cooperative_money = models.CharField(max_length=255, null=True, verbose_name='意向价格', blank=True)
    contact = models.CharField(max_length=255, null=True, verbose_name='联系人', blank=True)
    contact_info = models.CharField(max_length=255, null=True, verbose_name='联系方式', blank=True)
    technical_maturity = models.TextField(max_length=255, null=True, verbose_name='技术成熟度', blank=True)
    score = models.TextField(max_length=255, null=True, verbose_name='专利价值分级自评', blank=True)
    department = models.CharField(max_length=255, verbose_name='部门', null=True, blank=True)
    doip = models.TextField(verbose_name='本专利对应产品、技术优势、性能指标', blank=True)
    ctp = models.TextField(null=True, blank=True, verbose_name='产业化前景描述')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    zip_analysis_id = models.OneToOneField(ZipAnalysisResultModel, on_delete=models.CASCADE,
                                           db_column="zip_analysis_id", null=False, verbose_name='压缩包内容解析id')
    user_id = models.ForeignKey(UserModel, on_delete=models.SET(1), db_column="user_id", verbose_name='用户id',default=1)
    tech_score = models.CharField(max_length=255, verbose_name='技术分数', default="")
    market_score = models.CharField(max_length=255, verbose_name='市场分数', default="")
    law_score  = models.CharField(max_length=255, verbose_name='法律分数', default="")
    class Meta:
        db_table = 'result_export'
        verbose_name = '导出excl的列表'
        permissions = [
            ("batch_update", "批量修改excl内容"),
            ("export", "导出excl文件"),
        ]
