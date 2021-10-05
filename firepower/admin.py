from django.contrib import admin
from django.db.models import Sum, Avg
from django.db.models.functions import Coalesce
from django.contrib.admin.views.main import ChangeList
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from admin_totals.admin import ModelAdminTotals

from firepower import models

import utils

class FirearmResource(resources.ModelResource):
    class Meta:
        model = models.Firearm
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class FirearmAdmin(ImportExportModelAdmin):
    resource_class = FirearmResource
    list_display = ('number', 'mother_unit', 'operating_unit', 'category', 'nomenclature','servicable','unservicable','total', 'file_attachment', 'updated_at')
    list_filter = ('mother_unit', 'operating_unit', 'category', 'nomenclature', )
    search_fields = ('mother_unit', 'operating_unit', 'category', 'nomenclature',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class AmmunitionResource(resources.ModelResource):
    class Meta:
        model = models.Ammunition
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class AmmunitionAdmin(ImportExportModelAdmin):
    resource_class = AmmunitionResource
    list_display = ('number', 'mother_unit', 'category', 'nomenclature','servicable','unservicable','total', 'file_attachment', 'updated_at')
    list_filter = ('mother_unit', 'category', 'nomenclature', )
    search_fields = ('mother_unit', 'category', 'nomenclature',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class AccessoriesResource(resources.ModelResource):
    class Meta:
        model = models.Accessories
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class AccessoriesAdmin(ImportExportModelAdmin):
    resource_class = AccessoriesResource
    list_display = ('nomenclature', 'fssu_1','fssu_1_fsst','fssu_4','fssu_5','fssu_6','fssu_7','fssu_8','fssu_9', 'fssu_10','fssu_12','aabn','total', 'mindanao_area','visayas_area','luzon_area', 'file_attachment', 'updated_at')
    list_filter = ( 'nomenclature', )
    search_fields = ('nomenclature',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class SparePartsResource(resources.ModelResource):
    class Meta:
        model = models.SpareParts
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class SparePartsAdmin(ImportExportModelAdmin):
    resource_class = SparePartsResource
    list_display = ('nomenclature', 'fssu_1','fssu_1_fsst','fssu_4','fssu_5','fssu_6','fssu_7','fssu_8','fssu_9', 'fssu_10','fssu_12','aabn','total', 'mindanao_area','visayas_area','luzon_area', 'file_attachment', 'updated_at')
    list_filter = ( 'nomenclature', )
    search_fields = ('nomenclature',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class StatusOfFillUpResource(resources.ModelResource):
    class Meta:
        model = models.StatusOfFillUp
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class StatusOfFillUpAdmin(ImportExportModelAdmin):
    resource_class = StatusOfFillUpResource
    list_display = ('particular','toe_type','category','firearms','ammunition','table_of_equipment', 'pamu_fas_oh','ascom_fas_pa_stocks','total_fas_oh_pamu_pa_stocks','file_attachment', 'updated_at')
    list_filter = ( 'particular','toe_type','category','firearms','ammunition', )
    search_fields = ('particular','toe_type','category','firearms','ammunition',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class TOEPaWideResource(resources.ModelResource):
    class Meta:
        model = models.TOEPaWide
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class TOEPaWideAdmin(ImportExportModelAdmin):
    resource_class = TOEPaWideResource
    list_display = ('particular','toe_type','category','firearms','ammunition','table_of_equipment', 'pamu_fas_oh','variance','file_attachment', 'updated_at')
    list_filter = ( 'particular','toe_type','category','firearms','ammunition', )
    search_fields = ('particular','toe_type','category','firearms','ammunition',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class TOEMotherUnitResource(resources.ModelResource):
    class Meta:
        model = models.TOEMotherUnit
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class TOEMotherUnitAdmin(ImportExportModelAdmin):
    resource_class = TOEMotherUnitResource
    list_display = ('particular','toe_type','category','firearms','ammunition','table_of_equipment', 'fas_oh','file_attachment', 'updated_at')
    list_filter = ( 'particular','toe_type','category','firearms','ammunition', )
    search_fields = ('particular','toe_type','category','firearms','ammunition',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ProgramsProcurementResource(resources.ModelResource):
    class Meta:
        model = models.ProgramsProcurement
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class ProgramsProcurementAdmin(ImportExportModelAdmin):
    resource_class = ProgramsProcurementResource
    list_display = ('lnr','particular','year','qty_oum','abc','contract_bid_amount', 'residuals','bidder_proponent', 'contract_awardee','status','remarks','file_attachment','updated_at')
    list_filter = ( 'lnr','particular','year' )
    search_fields = ('lnr','particular','year')

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ProgramsRepairAndMaintenanceResource(resources.ModelResource):
    class Meta:
        model = models.ProgramsRepairAndMaintenance
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class ProgramsRepairAndMaintenanceAdmin(ImportExportModelAdmin):
    resource_class = ProgramsRepairAndMaintenanceResource
    list_display = ('lnr','particular','year','qty_oum','abc','contract_bid_amount', 'residuals','bidder_proponent', 'contract_awardee','status','remarks','file_attachment','updated_at')
    list_filter = ( 'lnr','particular','year' )
    search_fields = ('lnr','particular','year')

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ProgramsDisposalResource(resources.ModelResource):
    class Meta:
        model = models.ProgramsDisposal
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class ProgramsDisposalAdmin(ImportExportModelAdmin):
    resource_class = ProgramsDisposalResource
    list_display = ('nomenclature', 'fssu_1','fssu_1_fsst','fssu_4','fssu_5','fssu_6','fssu_7','fssu_8','fssu_9', 'fssu_10','fssu_12','aabn','total', 'mindanao_area','visayas_area','luzon_area', 'file_attachment', 'updated_at')
    list_filter = ( 'nomenclature', )
    search_fields = ('nomenclature',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ProgramsDemilitarizationResource(resources.ModelResource):
    class Meta:
        model = models.ProgramsDemilitarization
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class ProgramsDemilitarizationAdmin(ImportExportModelAdmin):
    resource_class = ProgramsDemilitarizationResource
    list_display = ('number','nomenclature','make','quantity','location','remarks', 'file_attachment','updated_at')
    list_filter = ( 'nomenclature', 'make', 'location', )
    search_fields = ('nomenclature', 'make', 'location',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ExpenditureAmmunitionResource(resources.ModelResource):
    class Meta:
        model = models.ExpenditureAmmunition
        exclude = ('date','created_by','updated_by', 'created_at', 'updated_at' )

class ExpenditureAmmunitionAdmin(ImportExportModelAdmin):
    resource_class = ExpenditureAmmunitionResource
    list_display = ('nomenclature','combat_operation','training','total','other_activity', 'file_attachment','updated_at')
    list_filter = ( 'nomenclature', 'combat_operation', 'training', )
    search_fields = ('nomenclature', 'combat_operation', 'training',)

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



admin.site.register(models.Firearm, FirearmAdmin)
admin.site.register(models.Ammunition, AmmunitionAdmin)
admin.site.register(models.Accessories, AccessoriesAdmin)
admin.site.register(models.SpareParts, SparePartsAdmin)
admin.site.register(models.StatusOfFillUp, StatusOfFillUpAdmin)
admin.site.register(models.TOEPaWide, TOEPaWideAdmin)
admin.site.register(models.TOEMotherUnit, TOEMotherUnitAdmin)
admin.site.register(models.ProgramsRepairAndMaintenance, ProgramsRepairAndMaintenanceAdmin)
admin.site.register(models.ProgramsProcurement, ProgramsProcurementAdmin)
admin.site.register(models.ProgramsDisposal, ProgramsDisposalAdmin)
admin.site.register(models.ProgramsDemilitarization, ProgramsDemilitarizationAdmin)
admin.site.register(models.ExpenditureAmmunition, ExpenditureAmmunitionAdmin)
admin.site.register(models.IncomingCommunication, IncomingCommunicationAdmin)
admin.site.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)