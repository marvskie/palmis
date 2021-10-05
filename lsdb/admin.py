from django.contrib import admin
from lsdb import models

class InternationalMilitaryAffairsActivityReportInline(admin.TabularInline):
    model = models.InternationalMilitaryAffairsActivityReport
    extra = 0
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )

class InternationalMilitaryAffairsActivityPhotoInline(admin.TabularInline):
    model = models.InternationalMilitaryAffairsActivityPhoto
    extra = 0
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )

class InternationalMilitaryAffairsActivityAdmin(admin.ModelAdmin):
    model = models.InternationalMilitaryAffairsActivity
    list_display = ( 'activity','activity_type','country','venue','remarks','file_attachment','updated_at')
    list_filter = ('activity','country','venue','activity_type', )
    search_fields = ('activity','country','venue','activity_type', )
    inlines=[InternationalMilitaryAffairsActivityPhotoInline, InternationalMilitaryAffairsActivityReportInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class LogisticsOfficersForumActivityReportInline(admin.TabularInline):
    model = models.LogisticsOfficersForumActivityReport
    extra = 0
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )

class LogisticsOfficersForumPhotoInline(admin.TabularInline):
    model = models.LogisticsOfficersForumPhoto
    extra = 0
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )

class LogisticsOfficersForumActivityAdmin(admin.ModelAdmin):
    model = models.LogisticsOfficersForumActivity
    list_display = ( 'activity','activity_type','participants','requirements','venue','remarks','file_attachment','updated_at')
    list_filter = ('activity','venue','activity_type', )
    search_fields = ('activity','venue','activity_type', )
    inlines=[LogisticsOfficersForumPhotoInline, LogisticsOfficersForumActivityReportInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class LogisticsStaffVisitReportInline(admin.TabularInline):
    model = models.LogisticsStaffVisitPhoto
    extra = 0
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )

class LogisticsStaffVisitPhotoInline(admin.TabularInline):
    model = models.LogisticsStaffVisitPhoto
    extra = 0
    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )

class LogisticsStaffVisitAdmin(admin.ModelAdmin):
    model = models.LogisticsStaffVisit
    list_display = ( 'activity','venue','remarks','file_attachment','updated_at')
    list_filter = ('activity','venue', )
    search_fields = ('activity','venue', )
    inlines=[LogisticsStaffVisitPhotoInline, LogisticsStaffVisitReportInline]

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ATRStrategicProgramsAdmin(admin.ModelAdmin):
    model = models.ATRStrategicPrograms
    list_display = ( 'program_name','review_type','remarks','file_attachment','updated_at')
    list_filter = ('program_name', )
    search_fields = ('program_name', )

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class CourseApplicationProcedureAdmin(admin.ModelAdmin):
    model = models.CourseApplicationProcedure
    list_display = ( 'course','remarks','file_attachment','updated_at')
    list_filter = ('course', )
    search_fields = ('course', )

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ApprovedResolutionsCourseAdmin(admin.ModelAdmin):
    model = models.ApprovedResolutionsCourse
    list_display = ( 'course', 'venue_school', 'rank_requirement','slot','report_date','end_date','remarks','file_attachment','updated_at')
    list_filter = ('course', 'venue_school', 'rank_requirement',)
    search_fields = ('course', 'venue_school', 'rank_requirement',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class LogisticsSchoolingAdmin(admin.ModelAdmin):
    model = models.LogisticsSchooling
    list_display = ( 'course', 'category','venue_school', 'rank_requirement','slot','report_date','end_date','remarks','file_attachment','updated_at')
    list_filter = ('course', 'category','venue_school', 'rank_requirement',)
    search_fields = ('course', 'category','venue_school', 'rank_requirement',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class ExecomPropertyAccountabilityPersonnelAdmin(admin.ModelAdmin):
    model = models.ExecomPropertyAccountabilityPersonnel
    list_display = ( 'first_name', 'middle_name','last_name', 'unit','remarks','file_attachment','updated_at')
    list_filter = ('first_name', 'middle_name','last_name', 'unit',)
    search_fields = ('first_name', 'middle_name','last_name', 'unit',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class SurveyBoardAdmin(admin.ModelAdmin):
    model = models.SurveyBoard
    list_display = ( 'subject', 'doc_type', 'date','remarks','file_attachment','updated_at')
    list_filter = ('subject', 'doc_type', 'date',)
    search_fields = ('subject', 'doc_type', 'date',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class CoaFindingsCAARAdmin(admin.ModelAdmin):
    model = models.CoaFindingsCAAR
    list_display = ( 'title', 'date', 'year','remarks','file_attachment','updated_at')
    list_filter = ('title', 'date', 'year',)
    search_fields = ('title', 'date', 'year',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

class CoaFindingsAOMAdmin(admin.ModelAdmin):
    model = models.CoaFindingsAOM
    list_display = ( 'title','aom_number', 'date', 'year','remarks','file_attachment','updated_at')
    list_filter = ('title', 'aom_number','date', 'year',)
    search_fields = ('title','aom_number', 'date', 'year',)

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

class LogisticsReferenceAdmin(admin.ModelAdmin):
    model = models.LogisticsReference
    list_display = ('title', 'reference_type', 'year', 'branch','code','date_promulgated','remarks','file_attachment','updated_at')
    list_filter = ('title', 'reference_type', 'year', 'branch','code','date_promulgated',)
    search_fields = ('title', 'reference_type', 'year', 'branch','code','date_promulgated',)

    exclude = ('created_by','updated_by', 'created_at', 'updated_at' )
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
            obj.updated_by = request.user
        if change and obj.id:
            obj.updated_by = request.user
        obj.save()

admin.site.register(models.InternationalMilitaryAffairsActivity, InternationalMilitaryAffairsActivityAdmin)
admin.site.register(models.LogisticsOfficersForumActivity, LogisticsOfficersForumActivityAdmin)
admin.site.register(models.LogisticsStaffVisit, LogisticsStaffVisitAdmin)
admin.site.register(models.ATRStrategicPrograms, ATRStrategicProgramsAdmin)
admin.site.register(models.CourseApplicationProcedure, CourseApplicationProcedureAdmin)
admin.site.register(models.ApprovedResolutionsCourse, ApprovedResolutionsCourseAdmin)
admin.site.register(models.LogisticsSchooling, LogisticsSchoolingAdmin)
admin.site.register(models.ExecomPropertyAccountabilityPersonnel, ExecomPropertyAccountabilityPersonnelAdmin)
admin.site.register(models.SurveyBoard, SurveyBoardAdmin)
admin.site.register(models.CoaFindingsAOM, CoaFindingsAOMAdmin)
admin.site.register(models.CoaFindingsCAAR, CoaFindingsCAARAdmin)
admin.site.register(models.IncomingCommunication, IncomingCommunicationAdmin)
admin.site.register(models.OutgoingCommunication, OutgoingCommunicationAdmin)
admin.site.register(models.LogisticsReference, LogisticsReferenceAdmin)
