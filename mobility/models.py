from django.db import models
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from commons.models import Serviceability, AcquisitionMode, Unit, MAJOR_ISLANDS, QUARTER_CHOICES, EVAL_FORMAT
from inventory.models import TransferRecord
from message.models import Message
import utils

TRANSPORT_TYPES = (
    ('GMA', 'Ground Mobility'),
    ('SMA', 'Sea Mobility'),
    ('AMA', 'Air Mobility')
)

REPAIR_IMPLEMENTATION = (
    ('MINOR', 'Minor'),
    ('MAJOR', 'Major')
)


class NomenclatureTire(models.Model):
    name = models.CharField(max_length=256, unique=True)
    transfer_records = GenericRelation(TransferRecord, related_query_name='tire')

    def __str__(self):
        return self.name


class NomenclatureBattery(models.Model):
    name = models.CharField(max_length=256, unique=True)
    transfer_records = GenericRelation(TransferRecord, related_query_name='battery')

    def __str__(self):
        return self.name


class Tonnage(models.Model):
    name = models.CharField(max_length=8, unique=True)
    order = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ('order', )
        verbose_name_plural = 'Tonnage'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)
    transport_type = models.CharField(max_length=8, choices=TRANSPORT_TYPES)
    prefix = models.CharField(max_length=4)
    code = models.CharField(max_length=8, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, models.CASCADE, related_name='types')
    prefix = models.CharField(max_length=4)
    code = models.CharField(max_length=8, unique=True)
    parent_type = models.ForeignKey('Type', models.CASCADE, related_name='sub_types', null=True, blank=True)

    def __str__(self):
        return f'{self.category.name}, {self.name} ({self.prefix})'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.parent_type_id:
            self.category = self.parent_type.category

        super().save(force_insert, force_update, using, update_fields)


class NomenclatureVehicle(models.Model):
    name = models.CharField(max_length=256)
    vehicle_type = models.ForeignKey(Type, models.DO_NOTHING, related_name='nomenclatures')
    tonnage = models.ForeignKey(Tonnage, models.DO_NOTHING, related_name='nomenclatures', null=True, blank=True)
    nomenclature = models.CharField(max_length=512, unique=True)

    def no_of_vehicles(self):
        return self.vehicle_records.count()

    def prefix(self):
        return self.vehicle_type.prefix

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        tonnage = f'{self.tonnage.name} Ton' if self.tonnage_id else ''
        self.nomenclature = f'{self.vehicle_type.category.name}, {self.vehicle_type.name}, {tonnage} {self.name}'
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.nomenclature


class VehicleRecord(models.Model):
    serial = models.PositiveIntegerField(null=True, blank=True)
    category = models.CharField(max_length=512)
    item_code = models.CharField(max_length=16, blank=True, null=True)
    plate_no = models.CharField(max_length=64, blank=True, null=True)
    nomenclature = models.CharField(max_length=512)
    engine_no = models.CharField(max_length=128, blank=True, null=True)
    chassis_no = models.CharField(max_length=32, blank=True, null=True)
    serviceability = models.CharField(max_length=512)
    mvf = models.CharField(max_length=32, blank=True, null=True)
    conduction_no = models.CharField(max_length=64, blank=True, null=True)
    acquisition_year = models.PositiveIntegerField(blank=True, null=True)
    acquisition_mode = models.ForeignKey(AcquisitionMode, models.DO_NOTHING, related_name='vehicle_records',
                                         blank=True, null=True)
    geographical_location = models.CharField(max_length=32, choices=MAJOR_ISLANDS, null=True, blank=True)
    location = models.CharField(max_length=128, null=True, blank=True)
    unit = models.ForeignKey(Unit, models.DO_NOTHING, null=True)
    has_bfp = models.BooleanField(default=False)
    unit_price = models.FloatField(blank=True, null=True)
    remarks = GenericRelation(Message, related_query_name='vehicle_record')

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('serial', 'nomenclature')

    def colored_serviceability(self):
        serviceability = self.serviceability
        desc = serviceability.name
        if serviceability.code == 'G':
            return format_html(EVAL_FORMAT.format(color='#009933', evaluation=desc))
        elif serviceability.code == 'Y':
            return format_html(EVAL_FORMAT.format(color='#FFCC00', evaluation=desc))
        elif serviceability.code == 'U':
            return format_html(EVAL_FORMAT.format(color='#7D7D7D', evaluation=desc))
        else:
            return format_html(EVAL_FORMAT.format(color='#FF4000', evaluation=desc))
    colored_serviceability.short_description = 'Serviceability'
    colored_serviceability.admin_order_field = 'serviceability'

    def __str__(self):
        return self.item_code

#    def save(self, force_insert=False, force_update=False, using=None,
#             update_fields=None):
#        if not self.serial:
#            prefix = self.nomenclature.vehicle_type.prefix
#            self.serial = VehicleRecord.objects.filter(nomenclature__vehicle_type__prefix=prefix).count() + 1
#        self.item_code = f'{self.nomenclature.vehicle_type.prefix}-{self.serial:04}'
#
#        if self.unit_price:
#            self.unit_price = round(self.unit_price, 2)
#
#        super().save(force_insert, force_update, using, update_fields)


class RepairRecord(models.Model):
    vehicle = models.ForeignKey(VehicleRecord, models.DO_NOTHING, related_name='repair_records')
    unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+')
    requested_on = models.DateField()
    completed_on = models.DateField(null=True, blank=True)
    implementation = models.CharField(max_length=8, choices=REPAIR_IMPLEMENTATION)
    authority = models.CharField(max_length=32, null=True, blank=True)
    advice_no = models.CharField(max_length=32, null=True, blank=True)
    period_covered = models.CharField(max_length=8, choices=QUARTER_CHOICES, null=True, blank=True)
    amount_released = models.FloatField()
    has_fur = models.BooleanField(default=False)
    asa_number = models.CharField(max_length=512)
    current_market_value = models.FloatField()

    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

# ============ NEW PALMIS MODELS 


class RegistrationStatus(models.Model):
    registration_status = models.CharField(max_length=150)
    plate_number = models.CharField(max_length=32)
    plate_number_type = models.CharField(max_length=32)
    vehicle = models.ForeignKey(VehicleRecord, models.DO_NOTHING, related_name='+')
    unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+')
    mv_file = models.FileField(upload_to=utils.PathAndRename('uploads/mobility/%Y/%m/'))
    registration_date = models.DateField()

    action = models.CharField(max_length=150, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Registration Records'
        verbose_name_plural = 'Registration Records'

    def __str__(self):
        return self.plate_number

class InsuranceSchedule(models.Model):
    insurance_status = models.CharField(max_length=150)
    vehicle = models.ForeignKey(VehicleRecord, models.DO_NOTHING, related_name='insurance_schedules')
    unit = models.ForeignKey(Unit, models.DO_NOTHING, related_name='+')
    mv_file = models.FileField(upload_to=utils.PathAndRename('uploads/mobility/%Y/%m/'))
    date_insured = models.DateField()

    action = models.CharField(max_length=150, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Insurance Schedule'
        verbose_name_plural = 'Insurance Schedules'

    def __str__(self):
        return self.vehicle_code


class DisposalRecord(models.Model):
    vehicle = models.ForeignKey(VehicleRecord, models.DO_NOTHING, related_name='disposal_records')
    nomenclature = models.CharField(max_length=512)
    chasis_number = models.CharField(max_length=512)
    plate_number = models.CharField(max_length=32)
    cognizant_depot = models.CharField(max_length=512)
    remarks = models.TextField()

    action = models.CharField(max_length=150, null=True)
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, models.DO_NOTHING, related_name='+', default=1)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'Disposal Records'
        verbose_name_plural = 'Disposal Records'

    def __str__(self):
        return self.plate_number
