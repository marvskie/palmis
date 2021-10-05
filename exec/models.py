from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from commons.models import Organization, Account

import utils
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampMixin):
    name = models.CharField(max_length=256)
    branch = models.ForeignKey(Organization, models.DO_NOTHING, related_name='+')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)

    def __str__(self):
        return self.branch.name + ' > ' + self.name
    
    def natural_key(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Categories"

class Task(TimeStampMixin):
    custom_id = models.IntegerField()
    title = models.CharField(max_length=256)
    description=models.TextField()
    location= models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    due_date = models.DateField(null=True)
    created_by = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    assigned_to = models.ForeignKey(Account, models.DO_NOTHING, related_name='+', null=True)
    branch = models.ForeignKey(Organization, models.DO_NOTHING, related_name='+', null=True)

    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title

# class Task(TimeStampMixin):
#     custom_id = models.IntegerField()
#     title = models.CharField(max_length=256)
#     description=models.TextField()
#     location= models.TextField()
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     due_date = models.DateField(null=True)
#     created_by = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
#     assigned_to = models.ForeignKey(Account, models.DO_NOTHING, related_name='+', null=True)
#     branch = models.ForeignKey(Organization, models.DO_NOTHING, related_name='+', null=True)

#     updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)

#     class Meta:
#         verbose_name = 'Task'
#         verbose_name_plural = 'Tasks'

#     def __str__(self):
#         return self.title

class FileAttachment(TimeStampMixin):
    branch = models.ForeignKey(Organization, models.DO_NOTHING, related_name='file_branch')
    category = models.ForeignKey(Category, models.DO_NOTHING, related_name='file_category')
    title = models.CharField(max_length=256)
    uploaded_by = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    file = models.FileField(upload_to=utils.PathAndRename('uploads/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return self.title
        
    
class FileComment(TimeStampMixin):
    text = models.TextField()
    created_by = models.ForeignKey(Account, models.DO_NOTHING, related_name='+')
    commented_file = models.ForeignKey(FileAttachment, models.DO_NOTHING, related_name='file_comments')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)

    @property
    def commented_by(self):
        return str(self.created_by.role)