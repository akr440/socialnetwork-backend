from django.urls import path
from . import views

urlpatterns = [
    path('polls/', views.CreatePoll.as_view()),
    path('polls/<int:poll_id>/', views.getPoll.as_view()),
    path('polls/<int:poll_id>/vote',views.VoteinPoll.as_view()),
    path('polls/<int:poll_id>/delete',views.DeletPoll.as_view()),
]
