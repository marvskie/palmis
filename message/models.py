from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    remarks = models.TextField()

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.remarks} / {self.created_by}'


class FileAttachment(models.Model):
    message = models.ForeignKey(Message, models.DO_NOTHING)
    title = models.CharField(max_length=256)
    file = models.FileField()

    def __str__(self):
        return self.title
