from django.urls import path
from . import views

urlpatterns = [
    path('chatroom/<int:user_id>/',views.CreateChatroom.as_view()),
    path('chatroom/',views.getChatrooms.as_view()),
    path('message/<int:chatroom_id>/',views.SendMessage.as_view())
   
]
