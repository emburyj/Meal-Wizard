from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')