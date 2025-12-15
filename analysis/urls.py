from django.urls import path, include
from rest_framework.routers import SimpleRouter

from analysis import views
from analysis.views import ChatContentResult, ProblemLabelList, ZipResultViewSet, ResultExportView, ScoreView

router = SimpleRouter()
router.register('zip_results', ZipResultViewSet, basename='zip_result')
router.register('result_export', ResultExportView, basename='result_export')
router.register('labels', ProblemLabelList, basename='labels')
router.register('zips', views.ZipViewSet, basename='zip')



urlpatterns = [
    path('get_session_chats/<int:session_id>', ChatContentResult.as_view(), name='ChatContentResult'),
    path('score', ScoreView.as_view(), name='score'),

    path('', include(router.urls)),

]
