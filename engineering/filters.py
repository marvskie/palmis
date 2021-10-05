import django_filters

from engineering import models


class RepairRecordFilter(django_filters.FilterSet):
    advice_no_q = django_filters.CharFilter(field_name='advice_no', lookup_expr='icontains')
    authority_q = django_filters.CharFilter(field_name='authority', lookup_expr='icontains')
    requested_year = django_filters.NumberFilter(field_name='requested_on__year')

    class Meta:
        model = models.RepairRecord
        fields = ('id', 'building', 'has_fur', 'advice_no_q', 'authority_q', 'requested_year')


class BuildingRecordFilter(django_filters.FilterSet):
    building_code_q = django_filters.CharFilter(field_name='building_code', lookup_expr='icontains')
    description_q = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    reservation_name_q = django_filters.CharFilter(field_name='reservation__name', lookup_expr='icontains')

    class Meta:
        model = models.BuildingRecord
        fields = ('id', 'reservation', 'building_code_q', 'description_q', 'reservation_name_q', 'unit', 'category')


class ReservationRecordFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    location_q = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    camp_administrator_q = django_filters.CharFilter(field_name='camp_administrator', lookup_expr='icontains')

    class Meta:
        model = models.ReservationRecord
        fields = ('id', 'name_q', 'location_q', 'region', 'camp_administrator_q')


# class CoProjectRecordFilter(django_filters.FilterSet):
#     project_name_q = django_filters.CharFilter(field_name='project_name', lookup_expr='icontains')
#     contractor_q = django_filters.CharFilter(field_name='contractor', lookup_expr='icontains')

#     class Meta:
#         model = models.CoProjectRecord
#         fields = ('id', 'status', 'project_name_q', 'end_user', 'object_code', 'contractor_q')
