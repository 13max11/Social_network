from django.contrib import admin
from .models import Entry, Comment, Like
# Register your models here.

admin.site.register(Entry)
admin.site.register(Comment)
admin.site.register(Like)
