from django.contrib import admin
from django.urls import path
import wepler.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', wepler.views.home, name = "home"),
    path('plus_signup/', wepler.views.plus_signup, name = "plus_signup"),
    path('plz_signup/', wepler.views.plz_signup, name = "plz_signup"),
]
