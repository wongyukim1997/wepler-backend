from django.urls import path, include
from rest_framework import routers
import board.views

urlpatterns = [
    path('hire_post/', board.views.hire_board),
    path('hire_list/', board.views.Hire_board_listView.as_view({'get' : 'list',})),
    path('hire_delete/<int:board_id>/', board.views.hire_delete),
    path('hire_update/<int:board_id>/', board.views.hire_update),
    path('hire_apply/<int:board_id>/', board.views.apply),
    path('hire_board_count/', board.views.list_count),
    path('hire_detail/<int:board_id>/', board.views.Hire_board_detail),
]