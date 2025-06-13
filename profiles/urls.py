from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.ListProfile.as_view()),
    path('<int:pk>',views.ProfileDetails.as_view())
]
