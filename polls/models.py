from django.db import models
from accounts.models import User

# poll=question
class Polls(models.Model):
    """
    Polls model which will have the user who created it, and the poll question
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="polls")
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ['-created_at']

    def __str__(self):
        return self.question
    

class PollOptions(models.Model):
    '''
    PollOPtions model which will have the option and the poll question
    '''
    poll=models.ForeignKey(Polls, on_delete=models.CASCADE,related_name="options")
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text
    

class Votes(models.Model):
    '''
    this Votes model will have the user who voted, the option he chose, and the question
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option=models.ForeignKey(PollOptions, on_delete=models.CASCADE,related_name="votes")
    poll = models.ForeignKey(Polls, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'poll')  # Prevent a user from voting multiple times in a poll

    def __str__(self):
        return f"{self.user.username} voted on {self.poll.question}"