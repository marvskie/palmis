from django.db import models
from django.contrib.auth.models import User
from commons.models import Unit, Pamu, Fssu, Serviceability
import utils
from firepower.constants import *

class FirearmCategory(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'Firearm categories'

    def __str__(self):
        return self.name


class FirearmType(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(FirearmCategory, models.DO_NOTHING, related_name='+', null=True)

    def __str__(self):
        return self.name


class FirearmNomenclature(models.Model):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(FirearmType, models.DO_NOTHING, related_name='+')

    def __str__(self):
        return self.name


class AmmunitionCategory(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = 'Ammunition categories'

    def __str__(self):
        return self.name


class AmmunitionType(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(AmmunitionCategory, models.DO_NOTHING, related_name='+', null=True)

    def __str__(self):
        return self.name


class AmmunitionNomenclature(models.Model):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(AmmunitionType, models.DO_NOTHING, related_name='+')

    def __str__(self):
        return self.name


# ============== NEW PALMIS MODELS 

class Firearm(models.Model):
    number = models.CharField(max_length=512)
    mother_unit = models.CharField(max_length=512)
    operating_unit = models.CharField(max_length=512)
    category = models.CharField(max_length=512)
    nomenclature = models.CharField(max_length=512)
    servicable = models.IntegerField()
    unservicable = models.IntegerField()
    total = models.IntegerField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))
   
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Firearm Inventory'
        verbose_name_plural = 'Firearm Inventory'

    def __str__(self):
        return self.nomenclature

class Ammunition(models.Model):
    number = models.CharField(max_length=512)
    mother_unit = models.CharField(max_length=512)
    nomenclature = models.CharField(max_length=512)
    particular = models.TextField()
    category = models.CharField(max_length=512)   
    servicable = models.IntegerField()
    unservicable = models.IntegerField()
    total = models.IntegerField()
    remarks = models.TextField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))
    
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ammunition Inventory'
        verbose_name_plural = 'Ammunition Inventory'

    def __str__(self):
        return self.nomenclature

class Accessories(models.Model):
    nomenclature = models.CharField(max_length=512)
    fssu_1 = models.IntegerField()
    fssu_1_fsst = models.IntegerField()
    fssu_4 = models.IntegerField()
    fssu_5 = models.IntegerField()
    fssu_6 = models.IntegerField()
    fssu_7 = models.IntegerField()
    fssu_8 = models.IntegerField()
    fssu_9 = models.IntegerField()
    fssu_10 = models.IntegerField()
    fssu_11 = models.IntegerField()
    fssu_12 = models.IntegerField()
    aabn = models.IntegerField()
    total = models.IntegerField()
    mindanao_area = models.IntegerField()
    visayas_area = models.IntegerField()
    luzon_area = models.IntegerField()
    action = models.TextField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))
    
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Accessories Inventory'
        verbose_name_plural = 'Accessories Inventory'

    def __str__(self):
        return self.nomenclature

class SpareParts(models.Model):
    nomenclature = models.CharField(max_length=512)
    fssu_1 = models.IntegerField()
    fssu_1_fsst = models.IntegerField()
    fssu_4 = models.IntegerField()
    fssu_5 = models.IntegerField()
    fssu_6 = models.IntegerField()
    fssu_7 = models.IntegerField()
    fssu_8 = models.IntegerField()
    fssu_9 = models.IntegerField()
    fssu_10 = models.IntegerField()
    fssu_11 = models.IntegerField()
    fssu_12 = models.IntegerField()
    aabn = models.IntegerField()
    total = models.IntegerField()
    mindanao_area = models.IntegerField()
    visayas_area = models.IntegerField()
    luzon_area = models.IntegerField()
    action = models.TextField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))
    
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Spare Parts Inventory'
        verbose_name_plural = 'Spare Parts Inventory'

    def __str__(self):
        return self.nomenclature

class StatusOfFillUp(models.Model):
    particular = models.TextField()
    toe_type = models.CharField(max_length=50, choices=TOE_TYPE)
    category = models.CharField(max_length=512)    
    firearms = models.CharField(max_length=512, default=None)
    ammunition = models.CharField(max_length=512, default=None)

    table_of_equipment = models.IntegerField()
    pamu_fas_oh = models.IntegerField()
    ascom_fas_pa_stocks = models.IntegerField()
    total_fas_oh_pamu_pa_stocks = models.IntegerField()
    percent_fas_pamu_ascom_stocks = models.FloatField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))

    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TOE Status of Fill-UP'
        verbose_name_plural = 'TOE Status of Fill-UP'

    def __str__(self):
        return self.particular

class TOEPaWide(models.Model):
    particular = models.TextField()
    toe_type = models.CharField(max_length=50, choices=TOE_TYPE)
    category = models.CharField(max_length=512)    
    firearms = models.CharField(max_length=512, default=None)
    ammunition = models.CharField(max_length=512, default=None)

    table_of_equipment = models.IntegerField()
    pamu_fas_oh = models.IntegerField()
    variance = models.IntegerField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TOE PA Wide'
        verbose_name_plural = 'TOE PA Wide'

    def __str__(self):
        return self.particular

class TOEMotherUnit(models.Model):
    mother_unit = models.CharField(max_length=512)
    particular = models.TextField()
    toe_type = models.CharField(max_length=50, choices=TOE_TYPE)
    category = models.CharField(max_length=512)    
    firearms = models.CharField(max_length=512, default=None)
    ammunition = models.CharField(max_length=512, default=None)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))

    table_of_equipment = models.IntegerField()
    fas_oh = models.IntegerField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'TOE Mother Unit'
        verbose_name_plural = 'TOE Mother Unit'

    def __str__(self):
        return self.particular

class ProgramsProcurement(models.Model):
    lnr = models.CharField(max_length=512)
    particular = models.TextField()
    year = models.IntegerField()
    qty_oum = models.CharField(max_length=512)    
    abc = models.FloatField()
    contract_bid_amount = models.FloatField()
    residuals = models.CharField(max_length=512)
    bidder_proponent = models.CharField(max_length=512)
    contract_awardee = models.CharField(max_length=512)
    status = models.CharField(max_length=512)
    remarks = models.TextField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Procurement Programs'
        verbose_name_plural = 'Procurement Programs'

    def __str__(self):
        return self.particular

class ProgramsRepairAndMaintenance(models.Model):
    lnr = models.CharField(max_length=512)
    particular = models.TextField()
    year = models.IntegerField()
    qty_oum = models.CharField(max_length=512)    
    abc = models.FloatField()
    contract_bid_amount = models.FloatField()
    residuals = models.CharField(max_length=512)
    bidder_proponent = models.CharField(max_length=512)
    contract_awardee = models.CharField(max_length=512)
    status = models.CharField(max_length=512)
    remarks = models.TextField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Repair and Maintenance Programs'
        verbose_name_plural = 'Repair and Maintenance Programs'

    def __str__(self):
        return self.particular

class ProgramsDisposal(models.Model):
    nomenclature = models.CharField(max_length=512)
    fssu_1 = models.IntegerField()
    fssu_1_fsst = models.IntegerField()
    fssu_4 = models.IntegerField()
    fssu_5 = models.IntegerField()
    fssu_6 = models.IntegerField()
    fssu_7 = models.IntegerField()
    fssu_8 = models.IntegerField()
    fssu_9 = models.IntegerField()
    fssu_10 = models.IntegerField()
    fssu_11 = models.IntegerField()
    fssu_12 = models.IntegerField()
    aabn = models.IntegerField()
    total = models.IntegerField()
    mindanao_area = models.IntegerField()
    visayas_area = models.IntegerField()
    luzon_area = models.IntegerField()
    action = models.TextField()
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))

    
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Disposal Programs'
        verbose_name_plural = 'Disposal Programs'

    def __str__(self):
        return self.nomenclature

class ProgramsDemilitarization(models.Model):
    number = models.CharField(max_length=512)
    nomenclature = models.CharField(max_length=512)
    make = models.CharField(max_length=512)
    quantity = models.IntegerField()
    
    location = models.CharField(max_length=512)    
    remarks = models.TextField()
    action = models.CharField(max_length=512)    
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Demilitarization Programs'
        verbose_name_plural = 'Demilitarization Programs'

    def __str__(self):
        return self.nomenclature

class ExpenditureAmmunition(models.Model):
    nomenclature = models.CharField(max_length=512)
    combat_operation = models.CharField(max_length=512)
    training = models.CharField(max_length=512)
    
    total = models.IntegerField()    
    other_activity = models.TextField()
    action = models.CharField(max_length=512)
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))


    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ammunition Expenditures'
        verbose_name_plural = 'Ammunition Expenditures'

    def __str__(self):
        return self.nomenclature

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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Incoming Communication'

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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/firepower/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Outgoing Communication'
        
    def __str__(self):
        return self.subject