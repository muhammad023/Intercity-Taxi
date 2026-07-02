from django.contrib import admin
from django.urls import path
from apps.views import *

urlpatterns = [
    path("user/register", register_view, name="register"),
    path("user/otp", otp_view, name="otp_view"),
    path('login/', login_view, name='login'),

]
