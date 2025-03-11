from django.db import models
from django.conf import settings


# Create your models here.
class Review(models.Model):
    STATUS_CHOICES = [
        ('0','не преглянуто'),
        ('1','прийнято'),
        ('2','відхилено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='site_review')
    content = models.TextField()
    img = models.ImageField(upload_to='images/blog/', blank=True, null=True)

    status = models.CharField(max_length=32, 
                choices=STATUS_CHOICES, default='0')