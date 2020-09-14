from django.urls import path, include
from rest_framework import routers
import mypage.views

urlpatterns = [
    path('getMypage/', mypage.views.getMypage),
]