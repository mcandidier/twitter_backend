from django.contrib import admin
from .models import Profile, Tweet, Comment, Following, Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at',)
    readonly_fields = ('created_at',)

@admin.register(Tweet)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at',)
    readonly_fields = ('created_at', 'likes',)


admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Following)
