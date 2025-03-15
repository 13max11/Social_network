from django.db import models
from django.conf import settings

# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    img = models.ImageField(upload_to='images/blog/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return self.title

    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_comments')
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.entry}: {self.content[:25]}'

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_likes')
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='likes')

    def __str__(self) -> str:
        return f'{self.user} - {self.entry}'