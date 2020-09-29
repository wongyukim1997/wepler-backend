from django.urls import path, include
from rest_framework import routers
import mypage.views

urlpatterns = [
    path('getMypage/', mypage.views.getMypage),
    path('updateMypage/', mypage.views.update_user),
    path('apply_list/', mypage.views.Apply_list.as_view({'get' : 'list',})),
    path('accept/<int:apply_id>/', mypage.views.user_match),
    path('reject/<int:apply_id>/', mypage.views.apply_delete),
    path('apply_detail/<int:apply_id>/', mypage.views.apply_detail),
    path('match_list/', mypage.views.Match_list.as_view({'get' : 'list',})),
    path('complete/', mypage.views.match_complete),
    path('plus_complete_list/', mypage.views.Plus_match_complete_list.as_view({'get' : 'list',})),
    path('plz_complete_list/', mypage.views.Plz_match_complete_list.as_view({'get' : 'list',})),
]