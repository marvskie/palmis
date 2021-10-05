from django.contrib import admin
from adminbranch import models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from django.apps import apps

from django.contrib.admin.views.main import ChangeList
import utils

from django.contrib.admin import AdminSite

# class MyAdmin(AdminSite):
#    def app_index(self, request, app_label, extra_context=None):
#         app_models = apps.get_app_config(app_label).get_models()

#         if not extra_context:
#             extra_context = {}
#         extra_context['models'] = app_models
#         print(app_models)
#         extra_context['test'] = "test"

#         super().app_index(request, app_label, extra_context=extra_context)


class RosterOfTroopsResource(resources.ModelResource):
    class Meta:
        model = models.RosterOfTroops
        exclude = ('created_by','updated_by', 'created_at', 'updated_at' )


class RosterOfTroopsAdmin(ImportExportModelAdmin):
    resource_class = RosterOfTroopsResource
    list_display = ('last_name', 'first_name','middle_name', 'unit', 'title_position','branch','type_of_employment','soi','phs','saln','per','updated_at')
    list_filter = ('last_name', 'first_name','middle_name','unit', 'title_position','branch','type_of_employment',)
    search_fields = ('last_name', 'first_name','middle_name','unit', 'title_position','branch','type_of_employment',)
    
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

 

class AdminMooeAdmin(ImportExportModelAdmin):
    model = models.AdminMooe
    list_display = ('number', 'asa_number', 'title_of_document', 'quarter','status','year','file_attachment','updated_at',)
    list_filter = ('asa_number', 'title_of_document', 'quarter','status','year',)
    search_fields = ('asa_number', 'title_of_document', 'quarter','status','year',)
    
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class AdminEquipmentResource(resources.ModelResource):
    class Meta:
        model = models.AdminEquipment
        exclude = ('created_by','updated_by', 'created_at', 'updated_at' )


class AdminEquipmentAdmin(ImportExportModelAdmin):
    resource_class = AdminEquipmentResource
    list_display = ('number', 'type_of_equipment', 'modal_name', 'purpose','file_attachment','updated_at',)
    list_filter = ('type_of_equipment', 'modal_name', 'purpose',)
    search_fields = ('type_of_equipment', 'modal_name', 'purpose',)
    
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

admin.site.register(models.RosterOfTroops, RosterOfTroopsAdmin)
admin.site.register(models.AdminEquipment, AdminEquipmentAdmin)
admin.site.register(models.AdminMooe, AdminMooeAdmin)
admin.site.register(models.IncomingCommunication, IncomingCommunicationAdmin)
admin.site.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)

# MyAdmin.register(models.RosterOfTroops, RosterOfTroopsAdmin)
# MyAdmin.register(models.AdminEquipment, AdminEquipmentAdmin)
# MyAdmin.register(models.AdminMooe, AdminMooeAdmin)
# MyAdmin.register(models.IncomingCommunication, IncomingCommunicationAdmin)
# MyAdmin.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)