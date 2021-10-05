from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

import utils

from mobility import models


class TypeTabular(admin.TabularInline):
    model = models.Type
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'transport_type', 'code')
    search_fields = ('name', 'code', 'prefix')
    list_filter = ('transport_type', )
    inlines = (TypeTabular, )


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'code', 'parent_type')
    search_fields = ('name', 'code', 'prefix')
    list_filter = ('category', 'category__transport_type')
    autocomplete_fields = ['parent_type']
    ordering = ('category', 'parent_type', 'name')


class VehicleRecordTabular(admin.TabularInline):
    model = models.VehicleRecord
#    readonly_fields = ('colored_serviceability',)
    fields = ('item_code', 'acquisition_year', 'location', 'colored_serviceability')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'tonnage', 'no_of_vehicles')
    readonly_fields = ('nomenclature', 'prefix')
    search_fields = ('nomenclature', )
    list_filter = ('vehicle_type__category', 'vehicle_type', 'tonnage')
    inlines = [VehicleRecordTabular]
    autocomplete_fields = ['vehicle_type']
    ordering = ('vehicle_type', 'name')


class RepairRecordInline(admin.TabularInline):
    model = models.RepairRecord
    extra = 0
class RegistrationStatusInline(admin.TabularInline):
    model = models.RegistrationStatus
    extra = 0
class InsuranceScheduleInline(admin.TabularInline):
    model = models.InsuranceSchedule
    extra = 0
class DisposalRecordInline(admin.TabularInline):
    model = models.DisposalRecord
    extra = 0

class VehicleRecordResource(resources.ModelResource):
    class Meta:
        model = models.VehicleRecord
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class VehicleRecordAdmin(ImportExportModelAdmin):
    resource_class = VehicleRecordResource
    list_display = ('item_code','plate_no','engine_no','acquisition_year' )
    search_fields = ('item_code', 'nomenclature', 'engine_no', 'chassis_no')
#    readonly_fields = ('pamu', 'item_code')
    list_filter = ('serviceability', 'nomenclature', 'nomenclature',
                   'geographical_location', 'acquisition_year', 'acquisition_mode', 'has_bfp')
    autocomplete_fields = ['acquisition_mode', 'unit']
    ordering = ('nomenclature', 'item_code')
    inlines = [RepairRecordInline, RegistrationStatusInline, InsuranceScheduleInline, DisposalRecordInline]

#    def pamu(self, instance):
#        pamu = instance.unit.pamu.name
#        if instance.unit.alt_pamu_id:
#            pamu = f'{pamu}  / {instance.unit.alt_pamu.name}'
#        return pamu


class RepairRecordAdmin(admin.ModelAdmin):
    model = models.RepairRecord
    list_display = ('vehicle','unit','implementation','asa_number','period_covered', 'completed_on','amount_released','current_market_value' ,'has_fur', )
    list_filter = ('vehicle','unit','implementation','asa_number','period_covered',)
    search_fields = ('vehicle','unit','implementation','asa_number','period_covered',)
    autocomplete_fields = ['vehicle']

    # def item_code(self, instance):
    #     return instance.vehicle.item_code
    # item_code.short_description = 'Vehicle'
    # item_code.admin_order_field = 'vehicle'


    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()





# ==== NEW PALMIS

class DisposalRecordResource(resources.ModelResource):
    class Meta:
        model = models.DisposalRecord
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class DisposalRecordAdmin(ImportExportModelAdmin):
    resource_class = DisposalRecordResource
    list_display = ('vehicle', 'nomenclature', 'chasis_number', 'plate_number','cognizant_depot','remarks', 'updated_at')
    list_filter = ('vehicle', 'nomenclature', 'chasis_number', 'plate_number','cognizant_depot', )
    search_fields = ('vehicle', 'nomenclature', 'chasis_number', 'plate_number','cognizant_depot',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class InsuranceScheduleResource(resources.ModelResource):
    class Meta:
        model = models.InsuranceSchedule
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class InsuranceScheduleAdmin(ImportExportModelAdmin):
    resource_class = InsuranceScheduleResource
    list_display = ('vehicle', 'insurance_status', 'mv_file', 'unit','date_insured', 'updated_at')
    list_filter = ('vehicle', 'insurance_status', 'unit', )
    search_fields = ('vehicle', 'insurance_status', 'unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class RegistrationStatusResource(resources.ModelResource):
    class Meta:
        model = models.RegistrationStatus
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class RegistrationStatusAdmin(ImportExportModelAdmin):
    resource_class = RegistrationStatusResource
    list_display = ('vehicle', 'registration_status','plate_number', 'plate_number_type', 'mv_file', 'unit','registration_date', 'updated_at')
    list_filter = ('vehicle', 'registration_status','plate_number', 'plate_number_type', 'unit', )
    search_fields = ('vehicle', 'registration_status','plate_number', 'plate_number_type', 'unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

admin.site.register(models.InsuranceSchedule, InsuranceScheduleAdmin)
admin.site.register(models.DisposalRecord, DisposalRecordAdmin)
admin.site.register(models.RegistrationStatus, RegistrationStatusAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Type, TypeAdmin)
# admin.site.register(NomenclatureVehicle, NomenclatureAdmin)
# admin.site.register([Tonnage, NomenclatureTire, NomenclatureBattery])
admin.site.register(models.VehicleRecord, VehicleRecordAdmin)
admin.site.register(models.RepairRecord, RepairRecordAdmin)
