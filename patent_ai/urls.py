"""patent_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from celery import Celery

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^static/(?P<path>.*)$', static.serve,
    #   {'document_root': settings.STATIC_ROOT}, name='static'),
    path("", include("file.urls")),
    path("", include("analysis.urls")),
    path("", include("user.urls")),
    path('login', TokenObtainPairView.as_view(), name='login'),
]