from django.urls import path
from . import views

urlpatterns = [
    path('chatroom/<int:user_id>/',views.CreateChatroom.as_view()),
    path('chatroom/',views.getChatrooms.as_view()),
    path('message/<int:chatroom_id>/',views.SendMessage.as_view()),
    path('groupchatroom/',views.CreateAndFetchGroupChatroom.as_view()),
    path('groupchatroom/<int:group_id>/addmember/', views.AddMember.as_view()),
    path('groupchatroom/<int:group_id>/', views.GetGroup.as_view()),
    path('groupchatroom/<int:group_id>/removemember/', views.RemoveMember.as_view()),
    path('groupchatroom/<int:group_id>/exit/', views.ExitGroup.as_view()),
    path('groupchatroom/<int:group_id>/messages/', views.GetGroupMessages.as_view()),
]
