from django.db import models
from accounts.models import User
# Create your models here.

class Chatroom(models.Model):
    user1 = models.ForeignKey(User, related_name='chatrooms_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chatrooms_as_user2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Prevent duplicate chatrooms

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"
    

class Message(models.Model):
    chatroom=models.ForeignKey(Chatroom,related_name="messages",on_delete=models.CASCADE)
    sender= models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
        

class GroupChatroom(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='group_chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_group_chatrooms', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class GroupMessage(models.Model):
    group_chatroom = models.ForeignKey(GroupChatroom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} in {self.group_chatroom.name}: {self.content[:30]}"