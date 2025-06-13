from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('all/', views.PostLists.as_view()),
    path('',views.CreatePost.as_view()),
    path('<int:pk>/',views.PostDetailnUpdate.as_view())
]
