from rest_framework import serializers

from analysis.models import ZipAnalysisResultModel
from user.models import validate_positive, UserModel


class UserSerializer(serializers.ModelSerializer):
    all_analysis_count = serializers.IntegerField(validators=[validate_positive])
    auth_group = serializers.SerializerMethodField()
    analysis_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_superuser','all_analysis_count','analysis_count','auth_group']
    def get_analysis_count(self, obj):
        return ZipAnalysisResultModel.objects.filter(user_id=obj).count()

    def get_auth_group(self, obj):
        groups = UserModel.objects.get(id=obj.id).groups.all()
        if len(groups) > 0:
            return groups[0].name
        return None
