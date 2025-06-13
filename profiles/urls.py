from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.UserSignup.as_view()),
    path('login/',views.UserLogin.as_view())
]
