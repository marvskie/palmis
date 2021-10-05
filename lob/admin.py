from django.contrib import admin
from lob import models

class StatusReportInline(admin.TabularInline):
    model = models.StatusAccomplishmentReport
    extra = 0
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )


class StatusAccomplishmentReportsAdmin(admin.ModelAdmin):
    model = models.AccomplishmentReport
    list_display = ('title','pamu', 'subject','quarter','month', 'date_received','file_attachment','action','updated_at')
    list_filter = ('title','pamu', 'subject','quarter','month', )
    search_fields = ('title','pamu', 'subject','quarter','month', )
    inlines=[StatusReportInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class IssuesAndConcernsAdmin(admin.ModelAdmin):
    model = models.IssuesAndConcerns
    list_display = ('pamu', 'sub_unit','concerned_branch','issues_and_concerns','action_taken', 'remarks','date','file_attachment','updated_at')
    list_filter = ('pamu', 'sub_unit','concerned_branch','issues_and_concerns','action_taken', 'remarks',)
    search_fields = ('pamu', 'sub_unit','concerned_branch','issues_and_concerns','action_taken', 'remarks',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class CommandDirectedActivitiesAdmin(admin.ModelAdmin):
    model = models.CommandDirectedActivities
    list_display = ('activity', 'description', 'requirements', 'status','date','action','file_attachment','updated_at')
    list_filter = ('activity', 'description', 'status',)
    search_fields = ('activity', 'description', 'status',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class PCHTAdmin(admin.ModelAdmin):
    model = models.PCHT
    list_display = ('description', 'program_status', 'number','purpose','requirements','amount' ,'status','action','file_attachment','updated_at')
    list_filter = ('description', 'program_status', 'purpose','status',)
    search_fields = ('description', 'program_status', 'purpose','status',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class LogisticsSupportPlanAdmin(admin.ModelAdmin):
    model = models.LogisticsSupportPlan
    list_display = ('subject', 'plan_type', 'number','status','action','file_attachment', 'updated_at')
    list_filter = ('subject', 'plan_type','status',)
    search_fields = ('subject','subject', 'plan_type','status',)

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

admin.site.register(models.AccomplishmentReport, StatusAccomplishmentReportsAdmin)
admin.site.register(models.IssuesAndConcerns, IssuesAndConcernsAdmin)
admin.site.register(models.CommandDirectedActivities, CommandDirectedActivitiesAdmin)
admin.site.register(models.PCHT, PCHTAdmin)
admin.site.register(models.LogisticsSupportPlan, LogisticsSupportPlanAdmin)
admin.site.register(models.IncomingCommunication, IncomingCommunicationAdmin)
admin.site.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)
