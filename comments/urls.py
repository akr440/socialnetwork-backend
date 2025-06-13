from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:post_id>/comments/', views.AllCommentsListNCreate.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', views.CommentDetailNUpdate.as_view(), name='comment-detail'),
]
