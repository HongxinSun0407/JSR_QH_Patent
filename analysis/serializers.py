from analysis.models import *


class ProblemLabelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ProblemLabelModel
        fields = '__all__'


class ChatSessionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ChatSessionModel
        fields = ['id', 'create_time']


class ChatContentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ChatContentModel
        fields = ['id', 'create_time', 'role', 'content', 'session_id', 'group_id']


class ZipAnalysisSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ZipAnalysisModel
        fields = ['id', 'name', 'update_time', 'status', 'create_time', 'total', 'count', 'username']

    def get_count(self, obj):
        return ZipAnalysisResultModel.objects.filter(zip_id=obj).filter(status__in = ['success', 'error']).count()

    def get_username(self, obj)->str:
        return obj.user_id.username


class ZipAnalysisResultSerializer(serializers.ModelSerializer):
    zip_id = serializers.PrimaryKeyRelatedField(read_only=True)
    file_id = serializers.PrimaryKeyRelatedField(read_only=True)
    session_id = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ZipAnalysisResultModel
        fields = ['id', 'name', 'session_id', 'desc', 'status', 'generate_status', 'file_id', 'create_time', 'zip_id', 'rest_count']


class ResultExportSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    apply_code = serializers.CharField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    zip_analysis_id = serializers.PrimaryKeyRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ResultExportModel
        fields = '__all__'



