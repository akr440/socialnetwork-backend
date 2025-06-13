from django.db import models
from django.db.models.signals import post_save
from accounts.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    dob=models.DateField()
    content = models.TextField(blank=True,default="Welcome to your profile! Add some details about yourself.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance,dob=instance.date_of_birth)

post_save.connect(create_profile, sender=User)
