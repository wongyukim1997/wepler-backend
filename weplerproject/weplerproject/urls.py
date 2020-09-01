from django.contrib import admin
from django.urls import path
import wepler.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('plus_signup', wepler.views.Plus_signupView.as_view()),
    path('plz_signup', wepler.views.Plz_signupView.as_view()),
]
