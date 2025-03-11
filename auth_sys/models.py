from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, null=False)
    avatar = models.ImageField(upload_to='images/avatars/', default='images/avatars/default.jpg')
    description = models.TextField(blank=True, null=True)
    

    def __str__(self) -> str:
        return self.username