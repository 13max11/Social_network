from django.contrib import admin
from .models import Community, Community_rule, Community_folow, CommunityGroup, CommunityGroupItem, Post, Like, DisLike, Comment, PostView, CommunityView, BannedWord, AutoMessage
# Register your models here.

class CommunityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'created_by', 'slug')

class CommunityGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'creator', 'slug')

admin.site.register(Community, CommunityAdmin)
admin.site.register(Community_rule)
admin.site.register(Community_folow)
admin.site.register(CommunityGroup, CommunityGroupAdmin)
admin.site.register(CommunityGroupItem)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(DisLike)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(CommunityView)
admin.site.register(BannedWord)
admin.site.register(AutoMessage)

