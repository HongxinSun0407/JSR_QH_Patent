from django.urls import path, include
from rest_framework.routers import SimpleRouter

from user import views
router = SimpleRouter()
router.register('', views.UserView, basename='user')
urlpatterns = [
    path('', include(router.urls)),
]
