from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:post_id>/likes/', views.ListLikes.as_view()),
    path('posts/<int:post_id>/like/', views.CreateDeleteLikes.as_view()),
]
