import json


from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Profile
from django.contrib.auth.models import User

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Notification
from main.models import Like, Following, Comment


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def create_notification(user, message, action_user, content_type, object_id):
    Notification.objects.create(
        user=user,
        message=message,
        action_user=action_user,
        content_type=content_type,
        object_id=object_id,
    )


@receiver(post_save, sender=Following)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        message = f'{instance.user.username} started following you.'
        create_notification(
            user=instance.following,
            message=message,
            action_user=instance.user,
            content_type=ContentType.objects.get_for_model(Following),
            object_id=instance.id,
        )

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        message = f'{instance.user.username} liked your tweet: {instance.tweet.content}'
        create_notification(
            user=instance.tweet.user,
            message=message,
            action_user=instance.user,
            content_type=ContentType.objects.get_for_model(Like),
            object_id=instance.id,
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        message = f'{instance.user.username} commented on your tweet: {instance.content}'
        create_notification(
            user=instance.tweet.user,
            message=message,
            action_user=instance.user,
            content_type=ContentType.objects.get_for_model(Comment),
            object_id=instance.id,
        )


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        # send notification thru channel layer group
        # get channel layer then send the message 
        # @room_name_format: 'user-{instance.user.id}'
        if instance.action_user != instance.user:
            channel_layer = get_channel_layer()
            data = {
                'message': instance.message,
                'user': instance.action_user.id,
                'created_at': instance.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            }
            async_to_sync(channel_layer.group_send)(
                f'user_{instance.user.id}',
                {
                    'type': 'send_notification',
                    'message': json.dumps(data)
                }
            )
        
         
