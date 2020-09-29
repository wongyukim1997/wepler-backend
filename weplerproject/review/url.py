from django.urls import path, include
from rest_framework import routers
import review.views

urlpatterns = [
    path('review_post/', review.views.plus_review_post),
    path('plus_review_list/', review.views.Plus_review_list.as_view({'get' : 'list',})),
    path('plz_review_list/', review.views.Plz_review_list.as_view({'get' : 'list',})),
    path('plus_review_delete/<int:board_id>/', review.views.plus_review_delete),
    path('plz_review_delete/<int:board_id>/', review.views.plz_review_delete),
    path('plus_review_detali/<int:board_id>/', review.views.plus_review_detail),
    path('plz_review_detail/<int:board_id>/', review.views.plz_review_detail),
]
