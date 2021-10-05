import datetime
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from inventory.models import TransferRecord
from tosb.constants import *
import utils

class Pamu(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=64)
    pamu = models.ForeignKey(Pamu, models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Item(models.Model):
    type = models.ForeignKey(Type, models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=256, unique=True)
    unit = models.CharField(max_length=16, default='pc')

    def __str__(self):
        return self.name


class Nomenclature(models.Model):
    item = models.ForeignKey(Item, models.DO_NOTHING, null=True)
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Toe(models.Model):
    unit = models.ForeignKey(Unit, models.DO_NOTHING)
    item = models.ForeignKey(Item, models.DO_NOTHING, null=True)
    toe = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.unit.name


class Ats(models.Model):
    date = models.DateField(default=datetime.date.today)
    unit = models.ForeignKey(Unit, models.DO_NOTHING)
    ats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.unit.name


class Baseline(models.Model):
    date = models.DateField(default=datetime.date.today)
    unit = models.ForeignKey(Unit, models.DO_NOTHING)
    item = models.ForeignKey(Item, models.DO_NOTHING, null=True)
    baseline = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.unit.name


class IssuanceDirective(models.Model):
    date = models.DateField()
    series = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.series


class IssuanceDirectiveItem(models.Model):
    issuance_directive = models.ForeignKey(IssuanceDirective, models.DO_NOTHING)
    unit = models.ForeignKey(Unit, models.DO_NOTHING)
    nomenclature = models.ForeignKey(Nomenclature, models.DO_NOTHING)
    quantity = models.IntegerField(default=0)


class Transfer(models.Model):
    date = models.DateField()
    unit_source = models.ForeignKey(Unit, models.DO_NOTHING, related_name='transfer_outs')
    unit_recipient = models.ForeignKey(Unit, models.DO_NOTHING, related_name='transfer_ins')
    nomenclature = models.ForeignKey(Nomenclature, models.DO_NOTHING)
    quantity = models.IntegerField(default=0)


class NomenclatureIcie(models.Model):
    name = models.CharField(max_length=256)
    transfer_records = GenericRelation(TransferRecord, related_query_name='icie')

    def __str__(self):
        return self.name


# ==== NEW PALMIS MODELS

class TOSPolicies(models.Model):
    policy_type = models.CharField(max_length=8, choices=POLICY_TYPE, null=True, blank=True)
    branch = models.CharField(max_length=32)
    title = models.CharField(max_length=512)
    year = models.IntegerField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))


    action = models.CharField(max_length=150, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'TOS Policies'
        verbose_name_plural = 'TOS Policies'

    def __str__(self):
        return self.title

class IncomingCommunication(models.Model):
    from_branch = models.CharField(max_length=512)
    commo_type = models.CharField(max_length=512)
    number = models.CharField(max_length=512)
    control_number = models.CharField(max_length=512)
    date_received = models.DateTimeField(auto_now_add=False)
    unit_office = models.CharField(max_length=512)
    subject = models.CharField(max_length=512)
    remarks = models.CharField(max_length=512)
    received_by = models.CharField(max_length=512)
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Incoming Communication'
        verbose_name_plural = 'Incoming Communication'

    def __str__(self):
        return self.subject


class OutgoingCommunication(models.Model):
    commo_type = models.CharField(max_length=512)
    number = models.CharField(max_length=512)
    control_number = models.CharField(max_length=512)
    origin_branch_office_unit = models.CharField(max_length=512)
    subject = models.CharField(max_length=512)
    recepient_unit = models.CharField(max_length=512)
    date_received = models.DateTimeField(auto_now_add=False)
    remarks = models.CharField(max_length=512)
    received_by = models.CharField(max_length=512)
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Outgoing Communication'
        verbose_name_plural = 'Outgoing Communication'

    def __str__(self):
        return self.subject


class RMCRecord(models.Model):
    summary_year = models.IntegerField()
    project_type = models.CharField(max_length=100, choices=RMC_PROJECT_TYPE, null=True, blank=True)
    project_name = models.CharField(max_length=512)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    unit = models.CharField(max_length=512)
    status = models.CharField(max_length=512)
    date = models.DateField(auto_now_add=False)
    remarks = models.CharField(max_length=512)
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'RMC'
        verbose_name_plural = 'RMC'

    def __str__(self):
        return self.project_name

class ICIERecord(models.Model):
    summary_year = models.IntegerField()
    list_of_specification_in_out = models.CharField(max_length=50, choices=SPEC_IN_OUT, null=True, blank=True)
    list_of_specification_source = models.CharField(max_length=8, choices=SPEC_SOURCE, null=True, blank=True)
    project_name = models.CharField(max_length=512)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    unit = models.CharField(max_length=512)
    status = models.CharField(max_length=512)
    remarks = models.CharField(max_length=512)
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'ICIE'
        verbose_name_plural = 'ICIE'
        
    def __str__(self):
        return self.project_name


class OERecap(models.Model):
    item_name = models.CharField(max_length=512)
    on_hand = models.FloatField()
    balance = models.FloatField()
    ats = models.CharField(max_length=512)
    unit = models.CharField(max_length=512)
    fill_up_rate = models.FloatField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'OE Recap'
        verbose_name_plural = 'OE Recap'
        
    def __str__(self):
        return self.item_name

class OEProgramming(models.Model):
    item_name = models.CharField(max_length=512)
    on_hand = models.FloatField()
    balance = models.FloatField()
    ats = models.CharField(max_length=512)
    unit = models.CharField(max_length=512)
    fill_up_rate = models.FloatField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'OE Programming'
        verbose_name_plural = 'OE Programming'
        
    def __str__(self):
        return self.item_name


class OEMasterList(models.Model):
    item_name = models.CharField(max_length=512)
    ats = models.CharField(max_length=512)
    unit = models.CharField(max_length=512)
    total_price = models.FloatField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'OE Masterlist'
        verbose_name_plural = 'OE Masterlist'
        
    def __str__(self):
        return self.item_name

class OEStockStatus(models.Model):
    li = models.CharField(max_length=512)
    nomenclature = models.CharField(max_length=512)
    price = models.FloatField()
    beg_balance = models.FloatField()
    receipt = models.CharField(max_length=512)
    issuance = models.CharField(max_length=512)
    auth_id_number = models.CharField(max_length=512)
    date_accepted_issued = models.DateField()
    date_expiration = models.DateField()
    end_balance = models.FloatField()
    end_user = models.CharField(max_length=512)
    supplier_remarks = models.TextField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/tosb/%Y/%m/'))

    
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'OE Stock Status'
        verbose_name_plural = 'OE Stock Status'
        
    def __str__(self):
        return self.item_name