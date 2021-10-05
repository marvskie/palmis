from django.contrib import admin

from ppb.models import ExpenseClass, ObjectCode, MissionArea, MajorPap, SubPap, SuggestedPap, PawafItem, Kma, \
    Dpg, ProgramObjective, Pawaf, StrategicObjective, PbdgObjective, StrategicProgram, PawafItemView, \
    PawafItemEndUser, PawafItemBudgetBreakdown, FundRelease,FundReleaseItem, Status, FundReleaseAsa, FundReleaseAsaItem, \
    KeyProgram
from commons.admin import GenericNameCodeAdmin
from ppb.filters import *

from django.utils.html import format_html
from django.urls import reverse

class GenericSelectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order')
    search_fields = ('name', 'code')
    ordering = ('-order', )
    list_editable = ('order', )


class PbdgObjectiveInline(admin.TabularInline):
    model = PbdgObjective
    extra = 0


class StrategicObjectiveAdmin(admin.ModelAdmin):
    list_display = ('description', )
    search_fields = ('description', )
    inlines = (PbdgObjectiveInline, )


class StrategicProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', )
    search_fields = ('code', 'description')


class ProgramObjectiveInline(admin.TabularInline):
    model = ProgramObjective
    extra = 0


class DpgAdmin(admin.ModelAdmin):
    list_display = ('description', 'mission_area_group', 'mission_area', 'active')
    search_fields = ('description', )
    inlines = (ProgramObjectiveInline, )
    list_filter = ('mission_area__mission_area_group', 'mission_area')

    def mission_area_group(self, instance):
        return instance.mission_area.get_mission_area_group_display()


class MissionAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'mission_area_group', 'code')


class ObjectCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'expense_class')
    ordering = ('code', )
    list_filter = ('expense_class', )
    search_fields = ('description', )


class ReadOnlyInline(admin.TabularInline):
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class PAPInline(ReadOnlyInline):
    model = MajorPap
    fields = ('name', 'expenditure_program', 'pa_program', 'pa_sub_program', 'pa_function')


class SubPapInline(ReadOnlyInline):
    model = SubPap
    fields = ('name', )


class SuggestedPapInline(ReadOnlyInline):
    model = SuggestedPap
    fields = ('name', )


class MajorPapAdmin(admin.ModelAdmin):
    list_display = ('name', 'kma', 'fixed_cost')
    inlines = [SubPapInline]
    list_filter = ['expenditure_program', 'pa_program', 'pa_sub_program', 'pa_function', 'fixed_cost']
    search_fields = ('name',)
    ordering = ('id', )


class SubPapAdmin(admin.ModelAdmin):
    fields = ('name', 'major_pap')
    list_display = ('name', 'major_pap')
    inlines = [SuggestedPapInline]
    ordering = ('id', )
    search_fields = ('name',)


class SuggestedPapAdmin(admin.ModelAdmin):
    fields = ('name', 'sub_pap')
    list_display = ('name', 'sub_pap')
    ordering = ('id', )
    search_fields = ('name',)


class PawafAdmin(admin.ModelAdmin):
    list_display = ('year', 'ceiling', 'description','summary')
    search_fields = ('description', )
    list_filter = ('year', )

    def summary (self, obj):
        return format_html(
            '<a class="button" target="_blank" href="/api/v1/ppb/apb/{}/download/">Download Report</a>&nbsp;',
            obj.pk,
        )
    summary.short_description = 'Summary'
    summary.allow_tags = True 


class BudgetBreakdownInline(admin.StackedInline):
    model = PawafItemBudgetBreakdown
    readonly_fields = ('amount', 'physical_target')
    extra = 0


class PawafItemAdmin(admin.ModelAdmin):
    list_display = ('strategic_program', 'major_pap', 'suggested_pap', 'specific_pap', 'end_user', 'branch', 'amount', 'summary', 'utilization')
    list_filter = ('strategic_program','mission_area', 'is_mandatory', 'end_user',)
    search_fields = ('suggested_pap__name', )
    autocomplete_fields = ['suggested_pap', ]
    readonly_fields = ('amount_q1', 'amount_q2', 'amount_q3', 'amount_q4', 'amount',
                       'physical_target_q1', 'physical_target_q2', 'physical_target_q3', 'physical_target_q4',
                       'physical_target')
    ordering = ('strategic_program', 'suggested_pap__sub_pap__major_pap', 'suggested_pap', 'id')
    inlines = (BudgetBreakdownInline,)

    def major_pap(self, instance):
        return instance.suggested_pap.sub_pap.major_pap

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.save()

    def summary (self, obj):
        return format_html(
            '<a class="button" target="_blank" href="/api/v1/ppb/pawaf/{}/download/">Download Report</a>&nbsp;',
            obj.pk,
        )
    summary.short_description = 'Summary'
    summary.allow_tags = True 

    def utilization (self, obj):
        return format_html(
            '<a class="button" target="_blank" href="/api/v1/ppb/pawaf/{}/download_utilization/">Download Report</a>&nbsp;',
            obj.pk,
        )
    utilization.short_description = 'Utilization'
    utilization.allow_tags = True 


class PawafItemViewAdmin(admin.ModelAdmin):
    list_display = ('description', 'field_ref', 'order')
    list_editable = ('order', )
    ordering = ('order', )


class FundReleaseItemInline(admin.StackedInline):
    model = FundReleaseItem
    extra = 0

class FundReleaseAdmin(admin.ModelAdmin):
    list_display = ('rrf_no', 'date', 'action')
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')
    search_fields = ('rrf_no','date','status','specific_paps', 'budget'  )
    list_filter = ('date','status','specific_paps', 'budget', )
    ordering = ('rrf_no', )
    # filter_horizontal = ('specific_paps',)
    inlines = (FundReleaseItemInline, )
    
    def action (self, obj):
        return format_html(
            '<a class="button" target="_blank" href="/api/v1/ppb/fund_release/{}/download/">Download DF</a>&nbsp;',
            obj.pk,
        )
    action.short_description = 'Action'
    action.allow_tags = True 


# def make_published(modeladmin, request, queryset):
#     queryset.update(status='p')
# make_published.short_description = "Mark selected stories as published"

class FundReleaseAsaItemInline(admin.StackedInline):
    model = FundReleaseAsaItem
    extra = 0


class FundReleaseAsaAdmin(admin.ModelAdmin):
    list_display = ('advice_no', 'rrf_no', 'amount',)
    search_fields = ('advice_no', 'fund_releases__rrf_no','date_released', 'unit', 'servicing_mfo', 'fund_releases','is_withdrawal')
    list_filter = ('date_released', 'unit', 'servicing_mfo', 'fund_releases','is_withdrawal')
    autocomplete_fields = ('servicing_mfo', 'unit')
    filter_horizontal = ('fund_releases', )
    inlines = (FundReleaseAsaItemInline, )
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')
    # actions = [make_published]

    def rrf_no(self, instance=None):
        if instance:
            return ' / '.join(instance.fund_releases.values_list('rrf_no', flat=True))
        return ''
    rrf_no.short_description = 'RRF Nos.'

    # def release_summary (self, obj):
    #     return format_html(
    #         '<a class="button" target="_blank" href="/api/v1/ppb/report/rrf_summary/">Download</a>&nbsp;',
    #         obj.pk,
    #     )
    # action.short_description = 'Release Summary'
    # action.allow_tags = True

    def changelist_view(self, request, extra_context=None):
        response = super(FundReleaseAsaAdmin, self).changelist_view(request, extra_context)
        unit = request.GET.get('unit__id__exact', default=-1)
        mfo = request.GET.get('servicing_mfo__id__exact', default=-1)
        budget = request.GET.get('fund_releases__id__exact', default=1)
        extra_context = {
            'unit': unit, 
            'mfo':mfo,
            'budget':budget
        }
        try:
            response.context_data.update(extra_context)
        except Exception as e:
            pass
        return response



admin.site.register(Status, GenericSelectionAdmin)
admin.site.register(Pawaf, PawafAdmin)
admin.site.register(ObjectCode, ObjectCodeAdmin)
admin.site.register(MajorPap, MajorPapAdmin)
admin.site.register(SubPap, SubPapAdmin)
admin.site.register(SuggestedPap, SuggestedPapAdmin)
admin.site.register(PawafItem, PawafItemAdmin)
admin.site.register(MissionArea, MissionAreaAdmin)
admin.site.register(ExpenseClass, GenericSelectionAdmin)
admin.site.register(Kma, GenericNameCodeAdmin)
admin.site.register(Dpg, DpgAdmin)
admin.site.register(StrategicObjective, StrategicObjectiveAdmin)
admin.site.register(StrategicProgram, StrategicProgramAdmin)
admin.site.register(PawafItemView, PawafItemViewAdmin)
admin.site.register(FundRelease, FundReleaseAdmin)
admin.site.register(FundReleaseAsa, FundReleaseAsaAdmin)
admin.site.register(KeyProgram, GenericSelectionAdmin)
admin.site.register([PawafItemEndUser,PbdgObjective,ProgramObjective,FundReleaseAsaItem, FundReleaseItem])
