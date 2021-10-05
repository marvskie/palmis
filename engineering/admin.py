from django.contrib import admin
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from django.contrib.admin.views.main import ChangeList
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from admin_totals.admin import ModelAdminTotals

import utils
from engineering import models
from commons.admin import GenericNameCodeAdmin



class RepairRecordInline(admin.TabularInline):
    model = models.RepairRecord
    extra = 0


class BuildingAdmin(admin.ModelAdmin):
    model = models.BuildingRecord
    list_display = ('building_code', 'description', 'unit')
    search_fields = ('building_code', 'description')
    list_filter = ('category', 'unit__pamu')
    inlines = [RepairRecordInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

# class CoProjectAdmin(admin.ModelAdmin):
#     model = models.CoProjectRecord
#     list_display = ('project_name', 'status', 'end_user', 'contractor')


class ReservationAdmin(admin.ModelAdmin):
    model = models.ReservationRecord
    list_display = ('name', 'location', 'camp_administrator', 'region', 'lot_area')
    list_filter = ('region', )
    search_fields = ('name', 'location', 'camp_administrator')

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

admin.site.register(models.BuildingRecord, BuildingAdmin)
admin.site.register(models.ReservationRecord, ReservationAdmin)
# admin.site.register(models.CoProjectRecord, CoProjectAdmin)
# admin.site.register(models.CoStatus, GenericNameCodeAdmin)
admin.site.register([models.BuildingCategory])


# == NEW PALMIS 

class HeavyEquipmentResource(resources.ModelResource):
    class Meta:
        model = models.HeavyEquipment
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class HeavyEquipmentAdmin(ImportExportModelAdmin):
    # model = models.HeavyEquipment
    resource_class = HeavyEquipmentResource
    list_display = ('particular', 'unit', 'date', 'amount', 'remark','updated_at')
    list_filter = ('particular','unit', )
    search_fields = ('particular','unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()
    
class LightEquipmentAdmin(ImportExportModelAdmin):
    model = models.LightEquipment
    list_display = ('particular', 'unit', 'date', 'amount', 'remark','updated_at')
    list_filter = ('particular','unit', )
    search_fields = ('particular','unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()
    
class LightRecordAdmin(ImportExportModelAdmin):
    model = models.LightRecord
    list_display = ('unit', 'end_user','service_provider', 'date', 'previous_billing','current_billing', 'amount', 'remark','updated_at')
    list_filter = ('unit', 'end_user','service_provider', )
    search_fields = ('unit', 'end_user','service_provider',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class WaterRecordAdmin(ImportExportModelAdmin):
    model = models.WaterRecord
    list_display = ('unit', 'end_user','service_provider', 'date', 'previous_billing','current_billing', 'amount', 'remark','updated_at')
    list_filter = ('unit', 'end_user','service_provider', )
    search_fields = ('unit', 'end_user','service_provider',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class InsuranceOfBuildingAdmin(ImportExportModelAdmin):
    model = models.InsuranceOfBuilding
    list_display = ('name_of_building','building_code','unit', 'floor_area_sqm','date_constructed','estimated_premium', 'date','amount', 'remark','updated_at')
    list_filter = ('name_of_building','building_code','unit', )
    search_fields = ('name_of_building','building_code','unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class SurveyTitlingFencingAdmin(ImportExportModelAdmin):
    model = models.SurveyTitlingFencing
    list_display = ('end_user','camp','name_location','requirement','unit', 'date','amount', 'remark','updated_at')
    list_filter = ('end_user','camp','name_location','requirement','unit', )
    search_fields = ('end_user','camp','name_location','requirement','unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class LotRentalAdmin(ImportExportModelAdmin):
    model = models.LotRental
    list_display = ('description','unit', 'date','amount', 'remark')
    list_filter = ('unit', )
    search_fields = ('description','unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class DetailedArchitecturalAndEngineeringDesignAdmin(ImportExportModelAdmin):
    model = models.DetailedArchitecturalAndEngineeringDesign
    list_display = ('particular','originator','end_user', 'projection_cost','date','remark','updated_at')
    list_filter = ('particular','originator','end_user', )
    search_fields = ('particular','originator','end_user',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ComprehensiveMasterDevelopmentPlanAdmin(ImportExportModelAdmin):
    model = models.ComprehensiveMasterDevelopmentPlan
    list_display = ('particular','originator','end_user', 'projection_cost','lot_area_sqm','date','remark','updated_at')
    list_filter = ('particular','originator','end_user', 'projection_cost','lot_area_sqm',)
    search_fields = ('particular','originator','end_user', 'projection_cost','lot_area_sqm',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class CapitalOutlayAdmin(ImportExportModelAdmin):
    model = models.CapitalOutlay
    list_display = ('number', 'project_name_location','projection_cost','prad','supplier','notice_of_award','etoc','percent_accomplishment','date_started','date_completed','remark','updated_at')
    list_filter = ('number', 'project_name_location','prad','supplier','notice_of_award',)
    search_fields = ('number', 'project_name_location','prad','supplier','notice_of_award',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class InteragencyTransferFundAdmin(ImportExportModelAdmin):
    model = models.InteragencyTransferFund
    list_display = ('number', 'project_name_location','projection_cost','prad','supplier','notice_of_award','etoc','percent_accomplishment','date_started','date_completed','remark','updated_at')
    list_filter = ('number', 'project_name_location','prad','supplier','notice_of_award',)
    search_fields = ('number', 'project_name_location','prad','supplier','notice_of_award',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class BasesConversionAndDevelopmentAuthorityAdmin(ImportExportModelAdmin):
    model = models.BasesConversionAndDevelopmentAuthority
    list_display = ('number', 'project_name_location','projection_cost','prad','supplier','notice_of_award','etoc','percent_accomplishment','date_started','date_completed','remark','updated_at')
    list_filter = ('number', 'project_name_location','prad','supplier','notice_of_award',)
    search_fields = ('number', 'project_name_location','prad','supplier','notice_of_award',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class IncomingCommunicationAdmin(ImportExportModelAdmin):
    model = models.IncomingCommunication
    list_display = ('number', 'subject', 'unit_office', 'from_branch','commo_type','control_number','date_received','received_by','file_attachment','remarks','updated_at')
    list_filter = ('unit_office', 'from_branch','commo_type','control_number',)
    search_fields = ('subject','unit_office', 'from_branch','commo_type','control_number',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class OutgoingCommunicationAdmin(ImportExportModelAdmin):
    model = models.OutgoingCommunication
    list_display = ('number', 'subject', 'recepient_unit', 'origin_branch_office_unit','commo_type','control_number','date_received','received_by','file_attachment','remarks','updated_at')
    list_filter = ('recepient_unit', 'origin_branch_office_unit','commo_type','control_number',)
    search_fields = ('subject','recepient_unit', 'origin_branch_office_unit','commo_type','control_number',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()


admin.site.register(models.HeavyEquipment, HeavyEquipmentAdmin)
admin.site.register(models.LightEquipment, LightEquipmentAdmin)
admin.site.register(models.LightRecord, LightRecordAdmin)
admin.site.register(models.WaterRecord, WaterRecordAdmin)
admin.site.register(models.InsuranceOfBuilding, InsuranceOfBuildingAdmin)
admin.site.register(models.SurveyTitlingFencing, SurveyTitlingFencingAdmin)
admin.site.register(models.LotRental, LotRentalAdmin)
admin.site.register(models.DetailedArchitecturalAndEngineeringDesign, DetailedArchitecturalAndEngineeringDesignAdmin)
admin.site.register(models.ComprehensiveMasterDevelopmentPlan, ComprehensiveMasterDevelopmentPlanAdmin)
admin.site.register(models.CapitalOutlay, CapitalOutlayAdmin)
admin.site.register(models.InteragencyTransferFund, InteragencyTransferFundAdmin)
admin.site.register(models.BasesConversionAndDevelopmentAuthority, BasesConversionAndDevelopmentAuthorityAdmin)
admin.site.register(models.IncomingCommunication, IncomingCommunicationAdmin)
admin.site.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)