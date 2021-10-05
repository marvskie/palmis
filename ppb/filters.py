import django_filters
from django.db.models import Sum, F, OuterRef, Subquery
from django.db.models.functions import Coalesce

import ppb.models
import ppb.consts
from utils import Round, InListFilter


class ByFundReleaseFilter(django_filters.Filter):
    def __init__(self, inner_field):
        super().__init__()
        self.inner_field = inner_field

    def filter(self, qs, value):
        if not value:
            return qs
        try:
            fund_release = ppb.models.FundRelease.objects.get(pk=value or 0)
        except ppb.models.FundRelease.DoesNotExist:
            return qs

        field = self.inner_field
        ids = fund_release.specific_paps.all().values_list(field, flat=True).distinct(field)

        return qs.filter(pk__in=ids)


class ReleaseFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value is None:
            return qs
        elif value not in ['partial', 'full', 'inconsistent', 'exceed', 'none']:
            return ppb.models.FundRelease.objects.none()

        amount = Round(Coalesce(Sum('release_items__release_recipients__amount'), 0.0))
        qs = qs.exclude(status__code=ppb.consts.RRF_CANCELLED)
        qs = qs.annotate(
            _released=Coalesce(Subquery(
                ppb.models.FundReleaseAsaItem.objects.filter(release_item__fund_release_id=OuterRef('pk')).
                    values('release_item__fund_release_id').annotate(_t_sum=Sum('amount')).values('_t_sum')), 0.0),
            _amount=amount)

        if value == 'partial':
            return qs.filter(_amount__gt=F('_released'), _released__gt=0)
        elif value == 'full':
            return qs.filter(_amount=F('_released'))
        elif value == 'none':
            return qs.filter(_amount__gt_released__gt=0)
        elif value in ['inconsistent', 'exceed']:
            return qs.filter(_amount__lt=F('_released'))

class ObjectCodeFilter(django_filters.FilterSet):
    description_q = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    fund_release = ByFundReleaseFilter('budget_breakdown__object_code')

    class Meta:
        model = ppb.models.ObjectCode
        fields = ('id', 'expense_class')


class MissionAreaFilter(django_filters.FilterSet):
    fund_release = ByFundReleaseFilter('mission_area')

    class Meta:
        model = ppb.models.MissionArea
        fields = ('id', 'mission_area_group')


class DpgFilter(django_filters.FilterSet):
    description_q = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = ppb.models.Dpg
        fields = ('id', 'mission_area', 'description_q')


class PbdgObjectiveFilter(django_filters.FilterSet):
    description_q = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = ppb.models.PbdgObjective
        fields = ('id', 'strategic_objective')


class ProgramObjectiveFilter(django_filters.FilterSet):
    description_q = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = ppb.models.ProgramObjective
        fields = ('id', 'dpg', 'description_q')


class MajorPapFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ppb.models.MajorPap
        fields = ('id', 'expenditure_program', 'pa_program', 'pa_sub_program', 'pa_function', 'kma',
                  'fixed_cost')


class SubPapFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = ppb.models.SubPap
        fields = ('id', 'major_pap')


class SuggestedPapFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    major_pap = django_filters.NumberFilter(field_name='sub_pap__major_pap_id')

    class Meta:
        model = ppb.models.SuggestedPap
        fields = ('id', 'sub_pap', 'major_pap')


class PawafFilter(django_filters.FilterSet):
    description_q = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = ppb.models.Pawaf
        fields = ('id', 'year', )


class PawafItemFilter(django_filters.FilterSet):
    major_pap = django_filters.NumberFilter(field_name='suggested_pap__sub_pap__major_pap')
    sub_pap = django_filters.NumberFilter(field_name='suggested_pap__sub_pap')
    strategic_objective = django_filters.CharFilter(
        field_name='pbdg_objective__strategic_objective')
    fixed_cost = django_filters.BooleanFilter(field_name='suggested_pap__sub_pap__major_pap__fixed_cost')
    specific_pap_q = django_filters.CharFilter(field_name='specific_pap', lookup_expr='icontains')
    object_code = django_filters.NumberFilter(field_name='budget_breakdown__object_code')
    branch_q = django_filters.CharFilter(field_name='branch', lookup_expr='icontains')

    class Meta:
        model = ppb.models.PawafItem
        fields = ('id', 'major_pap', 'sub_pap', 'suggested_pap', 'mission_area', 'expense_class',
                  'is_mandatory', 'program_objective', 'pbdg_objective', 'strategic_objective',
                  'strategic_program', 'fixed_cost', 'pawaf', 'end_user', 'object_code')


class FundReleaseFilter(django_filters.FilterSet):
    rrf_no_q = django_filters.CharFilter(field_name='rrf_no', lookup_expr='icontains')
    other_budget_q = django_filters.CharFilter(field_name='other_budget', lookup_expr='icontains')
    specific_pap_q = django_filters.CharFilter(
        field_name='specific_paps__specific_pap', lookup_expr='icontains', distinct=True)
    specific_purpose_q = django_filters.CharFilter(
        field_name='release_items__specific_purpose', lookup_expr='icontains', distinct=True)
    release = ReleaseFilter()

    class Meta:
        model = ppb.models.FundRelease
        fields = ('id', 'status', 'budget', 'cmd')


class FundReleaseItemFilter(django_filters.FilterSet):
    object_code_q = django_filters.CharFilter(field_name='object_code__description', lookup_expr='icontains')
    fund_release = InListFilter(field_name='fund_release', lookup_expr='in')
    specific_purpose_q = django_filters.CharFilter(field_name='specific_purpose', lookup_expr='icontains')

    class Meta:
        model = ppb.models.FundReleaseItem
        fields = ('id', )


class FundReleaseAsaFilter(django_filters.FilterSet):
    advice_no_q = django_filters.CharFilter(field_name='advice_no', lookup_expr='icontains')
    purpose_q = django_filters.CharFilter(field_name='purpose', lookup_expr='icontains')
    rrf_no_q = django_filters.CharFilter(field_name='fund_releases__rrf_no', lookup_expr='icontains', distinct=True)

    class Meta:
        model = ppb.models.FundReleaseAsa
        fields = ('id', 'unit', 'servicing_mfo', 'is_withdrawal')


class PawafItemBudgetBreakdownFilter(django_filters.FilterSet):
    pawaf = django_filters.NumberFilter(field_name='pawaf_item__pawaf_id')
    suggested_pap = django_filters.NumberFilter(field_name='pawaf_item__suggested_pap_id')
    specific_pap = django_filters.CharFilter(field_name='pawaf_item__specific_pap', lookup_expr='icontains')
    fund_release = ByFundReleaseFilter(inner_field='budget_breakdown')

    class Meta:
        model = ppb.models.PawafItemBudgetBreakdown
        fields = ('id', )
