from django.db import models
from accounts.models import User
from posts.models import Post

class Like(models.Model):
    """
    Like model to track likes on posts.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensures a user can like a post only once
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} liked {self.post}"
