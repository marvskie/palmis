from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from tosb import models
import utils

class NomenclatureTabular(admin.TabularInline):
    model = models.Nomenclature
    extra = 0


class ItemAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    inlines = (NomenclatureTabular,)
    list_display = ('name', 'type', 'unit')
    list_filter = ('type', )
    ordering = ('name', )


class UnitAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'pamu')
    list_filter = ('pamu', )
    ordering = ('name', )


class UnitTabular(admin.TabularInline):
    model = models.Unit
    extra = 0


class PamuAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    inlines = (UnitTabular,)


class ToeAdmin(admin.ModelAdmin):
    search_fields = ('unit__name', 'item__name')
    list_filter = ('unit__pamu', 'item')
    list_display = ('unit', 'item', 'toe')
    autocomplete_fields = ('unit', 'item')
    ordering = ('unit__name', )


class AtsAdmin(admin.ModelAdmin):
    search_fields = ('unit__name', )
    list_filter = ('unit__pamu', )
    list_display = ('unit',  'ats')
    autocomplete_fields = ('unit', )
    ordering = ('unit__name', )


class BaselineAdmin(admin.ModelAdmin):
    search_fields = ('unit__name', 'item__name')
    list_filter = ('unit__pamu', 'item')
    list_display = ('unit', 'item', 'baseline')
    autocomplete_fields = ('unit', 'item')
    ordering = ('unit__name', )


class NomenclatureAdmin(admin.ModelAdmin):
    search_fields = ('name', 'item__name')
    list_display = ('name', 'item')
    list_filter = ('item', )
    ordering = ('name', 'item')
    list_display = ('name', 'item', )
    list_filter = ('item', 'item__type')


# admin.site.register(Item, ItemAdmin)
# admin.site.register(Nomenclature, NomenclatureAdmin)
# admin.site.register(Unit, UnitAdmin)
# admin.site.register(Pamu, PamuAdmin)
# admin.site.register(Toe, ToeAdmin)
# admin.site.register(Baseline, BaselineAdmin)
# admin.site.register(Ats, AtsAdmin)
# admin.site.register([Type])


class TOSPoliciesResource(resources.ModelResource):
    class Meta:
        model = models.TOSPolicies
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class TOSPoliciesAdmin(ImportExportModelAdmin):
    resource_class = TOSPoliciesResource
    list_display = ('title', 'policy_type', 'branch','year', 'file_attachment', 'updated_at')
    list_filter = ('title', 'policy_type', 'branch','year', )
    search_fields = ('title', 'policy_type', 'branch','year',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class RMCRecordResource(resources.ModelResource):
    class Meta:
        model = models.RMCRecord
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class RMCRecordAdmin(ImportExportModelAdmin):
    resource_class = RMCRecordResource
    list_display = ('project_name', 'summary_year', 'project_type','quantity','total_price','unit','status','date','remarks' ,'file_attachment', 'updated_at')
    list_filter = ('project_name', 'summary_year', 'project_type','unit','status','date', )
    search_fields = ('project_name', 'summary_year', 'project_type','unit','status','date',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ICIERecordResource(resources.ModelResource):
    class Meta:
        model = models.ICIERecord
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class ICIERecordAdmin(ImportExportModelAdmin):
    resource_class = ICIERecordResource
    list_display = ('project_name', 'summary_year', 'list_of_specification_in_out','list_of_specification_source','total_price','unit','status','quantity','remarks' ,'file_attachment', 'updated_at')
    list_filter = ('project_name', 'summary_year', 'unit','status', )
    search_fields = ('project_name', 'summary_year', 'unit','status',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class OERecapResource(resources.ModelResource):
    class Meta:
        model = models.OERecap
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class OERecapAdmin(ImportExportModelAdmin):
    resource_class = OERecapResource
    list_display = ('item_name', 'on_hand', 'balance','ats','unit','fill_up_rate','file_attachment', 'updated_at')
    list_filter = ('item_name', 'unit', )
    search_fields = ('item_name', 'unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class OEProgrammingResource(resources.ModelResource):
    class Meta:
        model = models.OEProgramming
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class OEProgrammingAdmin(ImportExportModelAdmin):
    resource_class = OEProgrammingResource
    list_display = ('item_name', 'on_hand', 'balance','ats','unit','fill_up_rate','file_attachment', 'updated_at')
    list_filter = ('item_name', 'unit', )
    search_fields = ('item_name', 'unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class OEMasterListResource(resources.ModelResource):
    class Meta:
        model = models.OEMasterList
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class OEMasterListAdmin(ImportExportModelAdmin):
    resource_class = OEMasterListResource
    list_display = ('item_name', 'ats','unit','total_price','file_attachment', 'updated_at')
    list_filter = ('item_name', 'unit', )
    search_fields = ('item_name', 'unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class OEStockStatusResource(resources.ModelResource):
    class Meta:
        model = models.OEStockStatus
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class OEStockStatusAdmin(ImportExportModelAdmin):
    resource_class = OEStockStatusResource
    list_display = ('li', 'nomenclature', 'price','beg_balance','receipt','issuance','auth_id_number','date_accepted_issued','date_expiration','end_balance','end_user','supplier_remarks','file_attachment', 'updated_at')
    list_filter = ('li', 'nomenclature', 'receipt','issuance','auth_id_number','date_accepted_issued','date_expiration','end_user', )
    search_fields = ('li', 'nomenclature', 'receipt','issuance','auth_id_number','date_accepted_issued','date_expiration','end_user',)

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


admin.site.register(models.OEStockStatus, OEStockStatusAdmin)
admin.site.register(models.OEMasterList, OEMasterListAdmin)
admin.site.register(models.OEProgramming, OEProgrammingAdmin)
admin.site.register(models.OERecap, OERecapAdmin)
admin.site.register(models.ICIERecord, ICIERecordAdmin)
admin.site.register(models.RMCRecord, RMCRecordAdmin)
admin.site.register(models.TOSPolicies, TOSPoliciesAdmin)
admin.site.register(models.IncomingCommunication, IncomingCommunicationAdmin)
admin.site.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)