from django.contrib import admin
from camb import models

class SRDPPhotoInline(admin.TabularInline):
    model = models.SRDPPhoto
    extra = 0
class SRDPProjectFileInline(admin.TabularInline):
    model = models.SRDPProjectFile
    extra = 0

class DASPhotoInline(admin.TabularInline):
    model = models.DASPhoto
    extra = 0
class DASProjectFileInline(admin.TabularInline):
    model = models.DASProjectFile
    extra = 0
class DASProjectStatusInline(admin.TabularInline):
    model = models.DASProjectStatus
    extra = 0

class DASProjectStatusAcquisitionInline(admin.TabularInline):
    model = models.DASProjectStatusAcquisition
    extra = 0
class DASProjectStatusProcurementInline(admin.TabularInline):
    model = models.DASProjectStatusProcurement
    extra = 0
class DASProjectStatusContractFinalizationInline(admin.TabularInline):
    model = models.DASProjectStatusContractFinalization
    extra = 0
class DASProjectStatusContractImplementationInline(admin.TabularInline):
    model = models.DASProjectStatusContractImplementation
    extra = 0

class DASProjectStatusAdmin(admin.ModelAdmin):
    model = models.DASProjectStatus
    list_display = ('das_project','quantity','abc', 'twg', 'updated_at')
    list_filter = ('das_project','twg')
    search_fields = ('das_project','twg')
    inlines = [DASProjectStatusAcquisitionInline,DASProjectStatusProcurementInline,DASProjectStatusContractFinalizationInline,DASProjectStatusContractImplementationInline,]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class SRDPProjectsAdmin(admin.ModelAdmin):
    model = models.SRDPProjects
    list_display = ('project_name', 'abc','quality','supplier', 'contract_price','twg_name','contact_details','summary_file', 'updated_at')
    list_filter = ('project_name', 'twg_name','supplier',)
    search_fields = ('project_name', 'twg_name','supplier',)
    inlines = [SRDPPhotoInline, SRDPProjectFileInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class DASProjectsAdmin(admin.ModelAdmin):
    model = models.DASProjects
    list_display = ('project_name', 'abc','quality','supplier', 'contract_price','twg_name','contact_details','summary_file', 'updated_at')
    list_filter = ('project_name', 'twg_name','supplier',)
    search_fields = ('project_name', 'twg_name','supplier',)
    inlines = [DASPhotoInline, DASProjectFileInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class FMSPhotoInline(admin.TabularInline):
    model = models.FMSPhoto
    extra = 0

class FMSProjectsAdmin(admin.ModelAdmin):
    model = models.FMSProjects
    list_display = ('project_name', 'fms_case','quality','date_loa_accepted', 'status','summary', 'updated_at')
    list_filter = ('project_name', 'fms_case','quality', 'date_loa_accepted', 'status')
    search_fields = ('project_name','fms_case','quality', 'date_loa_accepted', 'status')
    inlines = [FMSPhotoInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class InternationalLogisticsActivitiesAdmin(admin.ModelAdmin):
    model = models.InternationalLogisticsActivities
    list_display = ('activity', 'description','status','date', 'file_attachment', 'updated_at')
    list_filter = ('activity', 'description','status', 'date')
    search_fields = ('activity','description','status', 'date')

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class DraftDocumentsAdmin(admin.ModelAdmin):
    model = models.DraftDocuments
    list_display = ('title', 'file_type', 'file_attachment', 'updated_at')
    list_filter = ('title', 'file_type',)
    search_fields = ('title','file_type',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ReferencesHelpfulLinksAdmin(admin.ModelAdmin):
    model = models.ReferencesHelpfulLinks
    list_display = ('name', 'url', 'file_attachment', 'updated_at')
    list_filter = ('name', 'url',)
    search_fields = ('name','url',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ReferencesDefenseExhibitsAdmin(admin.ModelAdmin):
    model = models.ReferencesDefenseExhibits
    list_display = ('name', 'url', 'file_attachment', 'updated_at')
    list_filter = ('name', 'url',)
    search_fields = ('name','url',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ReferencesPoliciesAdmin(admin.ModelAdmin):
    model = models.ReferencesPolicies
    list_display = ('subject', 'origin', 'file_attachment', 'updated_at')
    list_filter = ('subject', 'origin',)
    search_fields = ('subject','origin',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ReferencesBrochuresAdmin(admin.ModelAdmin):
    model = models.ReferencesBrochures
    list_display = ('subject', 'type_of_commodity', 'file_attachment', 'updated_at')
    list_filter = ('subject', 'type_of_commodity',)
    search_fields = ('subject','type_of_commodity',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()
class IncomingCommunicationAdmin(admin.ModelAdmin):
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

class OutgoingCommunicationAdmin(admin.ModelAdmin):
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

admin.site.register(models.SRDPProjects, SRDPProjectsAdmin)
admin.site.register(models.DASProjectStatus, DASProjectStatusAdmin)
admin.site.register(models.DASProjects, DASProjectsAdmin)
admin.site.register(models.FMSProjects, FMSProjectsAdmin)
admin.site.register(models.InternationalLogisticsActivities, InternationalLogisticsActivitiesAdmin)
admin.site.register(models.DraftDocuments, DraftDocumentsAdmin)
admin.site.register(models.ReferencesHelpfulLinks, ReferencesHelpfulLinksAdmin)
admin.site.register(models.ReferencesDefenseExhibits, ReferencesDefenseExhibitsAdmin)
admin.site.register(models.ReferencesPolicies, ReferencesPoliciesAdmin)
admin.site.register(models.ReferencesBrochures, ReferencesBrochuresAdmin)
admin.site.register(models.IncomingCommunication, IncomingCommunicationAdmin)
admin.site.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)


