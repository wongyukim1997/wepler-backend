from django.urls import path, include
from rest_framework import routers
import board.views

router = routers.DefaultRouter()
router.register('posts', board.views.TestPostView)

urlpatterns = [
    path('hire_post/', board.views.hire_board),
    path('hire_list/', board.views.Hire_board_listView.as_view({'get' : 'list',})),
    path('hire_apply/', board.views.apply),
    path('hire_detail/', board.views.Hire_board_detail),
]