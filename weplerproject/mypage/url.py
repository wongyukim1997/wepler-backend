from django.urls import path, include
from rest_framework import routers
import mypage.views

urlpatterns = [
    path('getMypage/', mypage.views.getMypage),
    path('updateMypage/', mypage.views.update_user),
    path('apply_list/', mypage.views.apply_list),
    path('accept/<int:apply_id>/', mypage.views.user_match),
    path('reject/<int:apply_id>/', mypage.views.apply_delete),
    path('apply_detail/<int:apply_id>/', mypage.views.apply_detail),
    path('match_list/', mypage.views.match_list),
    path('complete/<int:match_id>/', mypage.views.match_complete),
    path('match_detail/<int:match_id>/', mypage.views.match_detail),
    path('complete_detail/<int:match_id>/', mypage.views.match_detail),
    path('plus_complete_list/', mypage.views.plus_complete_list),
    path('plz_complete_list/', mypage.views.plz_complete_list),
]