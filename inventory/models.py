from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

from commons.models import Unit, Fssu, Pamu


class TransferStatus(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'Transfer statuses'

    def __str__(self):
        return self.name


class TransferType(models.Model):
    """
        Replenishment (transfer in, external source)
        Request (transfer in)
        Transfer (transfer out)
        Dispose (transfer out, external recipient)
    """
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class TransferRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    date = models.DateField()
    originating_unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+', null=True, blank=True)
    receiving_unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+', null=True, blank=True)

    transfer_type = models.ForeignKey(TransferType, models.DO_NOTHING, related_name='+')
    quantity = models.IntegerField()

    remarks = models.TextField(null=True, blank=True)

    fssu = models.ForeignKey(Fssu, models.DO_NOTHING, related_name='+', null=True, blank=True)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)
