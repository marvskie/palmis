from django.contrib import admin
from samb import models

from import_export.admin import ImportExportModelAdmin
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce

from django.contrib.admin.views.main import ChangeList
import utils

class PAProjectsInlineAdmin(admin.TabularInline):
    model = models.ProcurementActivityPAProject

class PITCProjectsInlineAdmin(admin.TabularInline):
    model = models.ProcurementActivityPITCProject

class PAProjectAdmin(ImportExportModelAdmin):
    model = models.PAProject
    list_display = ('project_title','fund_source', 'year', 'type_of_commodity' ,'unit_procurement_request_number','solicitation_number','mode_of_procurement','approved_budget_contract','supplier','bid_amount','current_status','file_attachment','updated_at')
    list_filter = ('fund_source', 'year', 'type_of_commodity' ,'unit_procurement_request_number','solicitation_number','mode_of_procurement','supplier','current_status',)
    search_fields = ('subject','fund_source', 'year', 'type_of_commodity' ,'unit_procurement_request_number','solicitation_number','mode_of_procurement','supplier','current_status',)
    inlines = [PAProjectsInlineAdmin]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class PITCProjectAdmin(ImportExportModelAdmin):
    model = models.PITCProject
    list_display = ('project_title','fund_source', 'year', 'type_of_commodity' ,'unit_procurement_request_number','solicitation_number','mode_of_procurement','approved_budget_contract','supplier','bid_amount','current_status','file_attachment','updated_at')
    list_filter = ('fund_source', 'year', 'type_of_commodity' ,'unit_procurement_request_number','solicitation_number','mode_of_procurement','supplier','current_status',)
    search_fields = ('subject','fund_source', 'year', 'type_of_commodity' ,'unit_procurement_request_number','solicitation_number','mode_of_procurement','supplier','current_status',)
    inlines = [PITCProjectsInlineAdmin]
    
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class BACRecordAdmin(ImportExportModelAdmin):
    model = models.BACRecord
    list_display = ('unit','name', 'bac_designation', 'contact_number' ,'remarks','file_attachment','updated_at')
    list_filter = ('unit','name', 'bac_designation',)
    search_fields = ('subject','unit','name', 'bac_designation',)
    
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()


class TWGRecordAdmin(ImportExportModelAdmin):
    model = models.TWGRecord
    list_display = ('unit','name', 'bac_designation', 'contact_number' ,'remarks','file_attachment','updated_at')
    list_filter = ('unit','name', 'bac_designation',)
    search_fields = ('subject','unit','name', 'bac_designation',)
    
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


admin.site.register(models.PAProject,PAProjectAdmin)
admin.site.register(models.PITCProject, PITCProjectAdmin)
admin.site.register(models.BACRecord, BACRecordAdmin)
admin.site.register(models.TWGRecord, TWGRecordAdmin)
admin.site.register(models.IncomingCommunication, IncomingCommunicationAdmin)
admin.site.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)