from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BannedWord, AutoMessage, Post, Comment
from notifications.models import Notification

from django.urls import reverse
import re

@receiver(post_save, sender=Post)
def check_banned_words(sender, instance, **kwargs):

    message = AutoMessage.objects.filter(community=instance.community)
    print(message)
    if message:
        Comment.objects.create(
            user = instance.community.created_by,
            post = instance,
            content = f'(сповішення згенероване автоматично) {message.first().message}',
        )

    #Удаляет объект, если в поле content есть запрещённое слово из базы.
    
    cleaned_content = re.sub(r'<[^>]+>', '', instance.content).lower()

    full_text = f"{instance.title.lower()} {cleaned_content}"

    banned_words = set(
        BannedWord.objects.filter(community=instance.community).values_list("word", flat=True)
    )   

    if any(word in full_text for word in banned_words):
        Notification.objects.create(
            user=instance.created_by,
            message=f"у вашому пості '{instance.title} виявлено заборонене в цьому ком'юніті слово пост було автоматично видалено'",
            url=f"{reverse('community', kwargs={'slug':instance.community.slug})}",
        )
        instance.delete()