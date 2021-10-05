from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

from commons.models import Region, Unit, QUARTER_CHOICES, Pamu
from ppb.models import ObjectCode
from message.models import Message
import utils

class ReservationRecord(models.Model):
    name = models.CharField(max_length=256, unique=True)
    location = models.TextField()
    region = models.ForeignKey(Region, models.DO_NOTHING, related_name='reservations')
    lot_area = models.FloatField()
    camp_administrator = models.CharField(max_length=128)
    code = models.CharField(max_length=16)
    remarks = GenericRelation(Message, related_query_name='reservation')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BuildingCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    order = models.IntegerField(default=100)

    class Meta:
        verbose_name_plural = 'Building categories'

    def __str__(self):
        return self.name


class BuildingRecord(models.Model):
    reservation = models.ForeignKey(ReservationRecord, models.DO_NOTHING, related_name='buildings')
    category = models.ForeignKey(BuildingCategory, models.DO_NOTHING, related_name='buildings')
    building_code = models.CharField(max_length=32, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+')
    remarks = GenericRelation(Message, related_query_name='building')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.building_code


class RepairRecord(models.Model):
    building = models.ForeignKey(BuildingRecord, models.DO_NOTHING, related_name='repair_records')
    unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+')
    requested_on = models.DateField()
    completed_on = models.DateField(null=True, blank=True)
    authority = models.CharField(max_length=32, null=True, blank=True)
    advice_no = models.CharField(max_length=32, null=True, blank=True)
    period_covered = models.CharField(max_length=8, choices=QUARTER_CHOICES, blank=True, null=True)
    amount_released = models.FloatField()
    has_fur = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)


# class CoStatus(models.Model):
#     code = models.CharField(max_length=16, unique=True)
#     name = models.CharField(max_length=32)
#     order = models.PositiveIntegerField()

#     class Meta:
#         verbose_name_plural = 'CO Statuses'

#     def __str__(self):
#         return self.name


# class CoProjectRecord(models.Model):
#     project_name = models.CharField(max_length=512)
#     end_user = models.ForeignKey(Unit, models.DO_NOTHING, related_name='co_projects')
#     original_cost = models.FloatField()
#     approved_budget = models.FloatField()
#     bid_amount = models.FloatField()
#     object_code = models.ForeignKey(ObjectCode, models.DO_NOTHING, related_name='co_projects')
#     status = models.ForeignKey(CoStatus, models.DO_NOTHING, related_name='+')
#     contractor = models.CharField(max_length=128, null=True, blank=True)
#     start_construction = models.DateField(null=True, blank=True)
#     target_completion = models.DateField(null=True, blank=True)
#     actual_completion = models.DateField(null=True, blank=True)
#     remarks = GenericRelation(Message, related_query_name='co_project')

#     created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
#     updated_at = models.DateTimeField(auto_now=True)

#     def bid_residual(self):
#         return self.approved_budget - self.bid_amount

#     class Meta:
#         verbose_name = 'Capital Outlay Project'

#     def __str__(self):
#         return self.project_name


# ============== NEW PALMIS MODELS 

class HeavyEquipment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    unit = models.CharField(max_length=512)
    particular = models.TextField()
    amount = models.FloatField()
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Heavy Equipment'

    def __str__(self):
        return self.particular

class LightEquipment(models.Model):
    date = models.DateTimeField(auto_now_add=False)
    unit = models.CharField(max_length=512)
    particular = models.TextField()
    amount = models.FloatField()
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Light Equipment'

    def __str__(self):
        return self.particular

class LightRecord(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    unit = models.CharField(max_length=512)
    end_user = models.TextField()
    service_provider = models.CharField(max_length=512)
    
    previous_billing = models.FloatField()
    current_billing = models.FloatField()
    amount = models.FloatField()
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Light Record'

    def __str__(self):
        return "Light Record: {}".format(self.end_user )

class WaterRecord(models.Model):
    date = models.DateTimeField(auto_now_add=False)
    unit = models.CharField(max_length=512)
    end_user = models.TextField()
    service_provider = models.CharField(max_length=512)
    
    previous_billing = models.FloatField()
    current_billing = models.FloatField()
    amount = models.FloatField()
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Water Record'

    def __str__(self):
        return "Water Record: {}".format(self.end_user )

class InsuranceOfBuilding(models.Model):
    date = models.DateTimeField(auto_now_add=False)
    unit = models.CharField(max_length=512)
    name_of_building = models.CharField(max_length=512)
    building_code = models.CharField(max_length=512)
    floor_area_sqm = models.FloatField()
    date_constructed = models.DateTimeField(auto_now_add=False)
    amount = models.FloatField()
    estimated_premium = models.CharField(max_length=512)
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Insurance of Building'

    def __str__(self):
        return self.name_of_building

class SurveyTitlingFencing(models.Model):
    date = models.DateTimeField(auto_now_add=False)
    unit = models.CharField(max_length=512)
    end_user = models.CharField(max_length=512)
    camp = models.CharField(max_length=512)
    name_location = models.CharField(max_length=512)
    requirement = models.TextField()
    amount = models.FloatField()
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Survey/Titling/Fencing'

    def __str__(self):
        return self.end_user

class LotRental(models.Model):
    date = models.DateTimeField(auto_now_add=False)
    unit = models.CharField(max_length=512)
    description = models.TextField()
    amount = models.FloatField()
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lot Rental'

    def __str__(self):
        return "Lot Rental: {}".format(self.unit)

class DetailedArchitecturalAndEngineeringDesign(models.Model):
    date = models.DateTimeField(auto_now_add=False)
    originator = models.CharField(max_length=512)
    end_user = models.CharField(max_length=512)
    particular = models.TextField()
    projection_cost = models.FloatField()
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Detailed Architectural and Engineering Design'

    def __str__(self):
        return self.particular

class ComprehensiveMasterDevelopmentPlan(models.Model):
    date = models.DateTimeField(auto_now_add=False)
    originator = models.CharField(max_length=512)
    end_user = models.CharField(max_length=512)
    particular = models.TextField()
    lot_area_sqm = models.FloatField()
    projection_cost = models.FloatField()
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comprehensive Master Development Plan'

    def __str__(self):
        return self.particular

class CapitalOutlay(models.Model):
    number = models.CharField(max_length=512)
    project_name_location = models.TextField()
    projection_cost = models.FloatField()
    prad = models.CharField(max_length=512)
    supplier = models.CharField(max_length=512)
    notice_of_award = models.CharField(max_length=512)
    date_started = models.DateTimeField(auto_now_add=False)
    etoc = models.CharField(max_length=512)
    date_completed = models.DateTimeField(auto_now_add=False)
    percent_accomplishment = models.FloatField()     
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Capital Outlay'

    def __str__(self):
        return self.project_name_location

class InteragencyTransferFund(models.Model):
    number = models.CharField(max_length=512)
    project_name_location = models.TextField()
    projection_cost = models.FloatField()
    prad = models.CharField(max_length=512)
    supplier = models.CharField(max_length=512)
    notice_of_award = models.CharField(max_length=512)
    date_started = models.DateTimeField(auto_now_add=False)
    etoc = models.CharField(max_length=512)
    date_completed = models.DateTimeField(auto_now_add=False)
    percent_accomplishment = models.FloatField()     
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Inter-Agency Transfer Fund'

    def __str__(self):
        return self.project_name_location

class BasesConversionAndDevelopmentAuthority(models.Model):
    number = models.CharField(max_length=512)
    project_name_location = models.TextField()
    projection_cost = models.FloatField()
    prad = models.CharField(max_length=512)
    supplier = models.CharField(max_length=512)
    notice_of_award = models.CharField(max_length=512)
    date_started = models.DateTimeField(auto_now_add=False)
    etoc = models.CharField(max_length=512)
    date_completed = models.DateTimeField(auto_now_add=False)
    percent_accomplishment = models.FloatField()     
    remark = models.TextField()
    action = models.CharField(max_length=512)

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bases Conversion And Development Authority'

    def __str__(self):
        return self.project_name_location

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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/eb/%Y/%m/'))


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
    file_attachment = models.FileField(upload_to=utils.PathAndRename('uploads/eb/%Y/%m/'))

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Outgoing Communication'

    def __str__(self):
        return self.subject
