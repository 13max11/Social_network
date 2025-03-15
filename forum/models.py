from django.db import models
from django.utils.text import slugify
from django.conf import settings
from unidecode import unidecode

from tinymce.models import HTMLField
# Create your models here.

class Community(models.Model):
    name = models.CharField(max_length=32, unique=True)
    icon = models.ImageField(upload_to='images/forum_icons/', default='images/forum_icons/default.jpg')
    background_image = models.ImageField(upload_to='images/forum_icons/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Community_rule(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='rules')

    title = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

class Community_folow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_follow')
    is_moderator = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user} - {self.community}'

class CommunityGroup(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='images/forum_icons/', default='images/forum_icons/group_default.png')
    private = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class CommunityGroupItem(models.Model):
    group = models.ForeignKey(CommunityGroup, on_delete=models.CASCADE, related_name='group_item')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='group_item') 

class Post(models.Model):
    title = models.CharField(max_length=128)
    content = HTMLField()
    image = models.ImageField(upload_to='images/forum/', blank=True, null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='post')
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()
    
    def rating_count(self):
        return self.likes.count() - self.dislikes.count()

    def comment_count(self):
        return self.comments.count()


    class Meta:
        ordering = ['-created_at']

# class Repost(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reposts')
#     community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='reposts')

#     created_at = models.DateTimeField(auto_now=True)
#     comment = models.CharField(max_length=128)



class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    def __str__(self) -> str:
        return f'{self.user} - {self.post}'

class DisLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dislikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')

    def __str__(self) -> str:
        return f'{self.user} - {self.post}'

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.user} - {self.post}: {self.content[:25]}'

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='viewed')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_viewed')

    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

class CommunityView(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='viewed')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_viewed')

    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        unique_together = ('user', 'community')

    def __str__(self):
        return f"{self.user.username} - {self.community.name}"

class BannedWord(models.Model):
    word = models.CharField(max_length=256)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='banned_word')

    def __str__(self):
        return f"{self.word} - {self.community.name}"

    class Meta:
        unique_together = ('word','community')

class AutoMessage(models.Model):
    community = models.OneToOneField(Community, on_delete=models.CASCADE, related_name='auto_message')
    message = models.TextField()