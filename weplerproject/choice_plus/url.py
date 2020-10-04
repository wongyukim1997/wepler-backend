from django.urls import path, include
from rest_framework import routers
import choice_plus.views

urlpatterns = [
    path('plus_profile_list/<slug:address>/', choice_plus.views.plus_profile_list),
    path('plus_profile_list_count/<slug:address>/', choice_plus.views.plus_profile_list_count),
    path('apply/<int:choice_id>/', choice_plus.views.apply),
    path('plus_profile_detail/<int:choice_id>/', choice_plus.views.plus_profile_detail),
]