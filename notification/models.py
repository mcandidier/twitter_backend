from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    action_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='action_notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.message
