from django.urls import path, include
from rest_framework import routers
import mypage.views

urlpatterns = [
    path('getMypage/', mypage.views.getMypage),
    path('updateMypage/', mypage.views.update_user),
    path('applied_list/', mypage.views.applied_list),
    path('apply_list/', mypage.views.apply_list),
    path('accept/<int:apply_id>/', mypage.views.user_match),
    path('reject/<int:apply_id>/', mypage.views.apply_delete),
    path('applied_detail/<int:apply_id>/', mypage.views.applied_detail),
    path('match_list/', mypage.views.match_list),
    path('complete/<int:match_id>/', mypage.views.match_complete),
    path('match_detail/<int:match_id>/', mypage.views.match_detail),
    path('complete_detail/<int:match_id>/', mypage.views.match_detail),
    path('complete_list/', mypage.views.complete_list),
    path('complete_list_count/', mypage.views.complete_list_count),
    path('applied_list_count/', mypage.views.applied_list_count),
    path('apply_list_count/', mypage.views.apply_list_count),
    path('match_list_count/', mypage.views.match_list_count),
]