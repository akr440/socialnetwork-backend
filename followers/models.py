from django.db import models
from accounts.models import User
from posts.models import Post

class Follow(models.Model):
    """
    Like model to track likes on posts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'followed_user')  # Ensures a user can like a post only once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"
