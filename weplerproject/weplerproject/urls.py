from django.contrib import admin
from django.urls import path, include
import wepler.views
import board.views
import mypage.views
import review.views
import choice_plus.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('plus_signup/', wepler.views.plus_signup),
    path('plz_signup/', wepler.views.plz_signup),
    path('login/', wepler.views.login),
    path('token_check/', wepler.views.tokenCheck),
    path('board/', include('board.url')),
    path('mypage/', include('mypage.url')),
    path('review/', include('review.url')),
    path('choice_plus/', include('choice_plus.url')),
]
