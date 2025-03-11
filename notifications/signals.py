from django.db.models.signals import post_save
from django.dispatch import receiver
from forum.models import Comment
from .models import Notification

from django.urls import reverse

@receiver(post_save, sender=Comment)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        post = instance.post
        print(instance.pk)

        Notification.objects.create(
            user=post.created_by,
            message=f"Новий коментар у пості '{post.title}'",
            url=f"{reverse('post', kwargs={'slug':post.community.slug, 'pk':post.pk})}#{instance.pk}",
        )