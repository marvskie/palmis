from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from commons.models import Branch

import utils


class FileAttachment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    title = models.CharField(max_length=256)
    file = models.FileField(upload_to=utils.PathAndRename('uploads/%Y/%m/'))


class InstructionRecord(models.Model):
    subject = models.CharField(max_length=512)
    description = models.TextField()
    due_date = models.DateField()
    attachments = GenericRelation(FileAttachment, related_query_name='instruction')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)


class InstructionRecipient(models.Model):
    instruction = models.ForeignKey(InstructionRecord, models.DO_NOTHING, related_name='recipients')
    branch = models.ForeignKey(Branch, models.DO_NOTHING, related_name='+')


class InstructionResponseType(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=8, unique=True)
    order = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name


class InstructionResponse(models.Model):
    instruction = models.ForeignKey(InstructionRecord, models.DO_NOTHING, related_name='responses')
    type = models.ForeignKey(InstructionResponseType, models.DO_NOTHING, related_name='+')
    comment = models.TextField()
    attachments = GenericRelation(FileAttachment, related_query_name='instruction')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)
