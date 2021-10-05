import django_filters

from mobility import models
from inventory.models import TransferRecord


class BatteryRecordFilter(django_filters.FilterSet):
    nomenclature_q = django_filters.CharFilter(field_name='battery__name', lookup_expr='icontains')

    class Meta:
        model = TransferRecord
        fields = ('id', 'fssu', 'nomenclature_q')


class TireRecordFilter(django_filters.FilterSet):
    nomenclature_q = django_filters.CharFilter(field_name='tire__name', lookup_expr='icontains')

    class Meta:
        model = TransferRecord
        fields = ('id', 'fssu', 'nomenclature_q')


class RepairRecordFilter(django_filters.FilterSet):
    authority_q = django_filters.CharFilter(field_name='authority', lookup_expr='icontains')
    advice_no_q = django_filters.CharFilter(field_name='advice_no', lookup_expr='icontains')
    requested_year = django_filters.NumberFilter(field_name='requested_on__year')

    class Meta:
        model = models.RepairRecord
        fields = ('id', 'vehicle', 'authority_q', 'advice_no_q', 'has_fur', 'implementation', 'period_covered',
                  'requested_year')


class VehicleRecordFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='nomenclature__vehicle_type__category')
    nomenclature_q = django_filters.CharFilter(field_name='nomenclature__nomenclature', lookup_expr='icontains')
    engine_no_q = django_filters.CharFilter(field_name='engine_no', lookup_expr='icontains')
    chassis_no_q = django_filters.CharFilter(field_name='chassis_no', lookup_expr='icontains')
    pamu = django_filters.NumberFilter(field_name='unit__pamu_id')
    location_q = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    item_code_q = django_filters.CharFilter(field_name='item_code', lookup_expr='icontains')
    conduction_no_q = django_filters.CharFilter(field_name='conduction_no', lookup_expr='icontains')
    ending = django_filters.CharFilter(field_name='plate_no', lookup_expr='endswith')
    remarks_q = django_filters.CharFilter(field_name='remarks__remarks', lookup_expr='icontains', distinct=True)

    class Meta:
        model = models.VehicleRecord
        fields = ('id', 'item_code_q', 'serviceability', 'geographical_location', 'acquisition_year',
                  'acquisition_mode', 'category', 'nomenclature_q', 'engine_no_q', 'chassis_no_q', 'unit', 'pamu',
                  'location_q', 'has_bfp', 'conduction_no_q', 'ending', 'remarks_q')


class NomenclatureFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='vehicle_type__category_id')
    transport_type = django_filters.CharFilter(field_name='vehicle_type__category__transport_type')
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    nomenclature_q = django_filters.CharFilter(field_name='nomenclature', lookup_expr='icontains')

    class Meta:
        model = models.NomenclatureVehicle
        fields = ('id', 'vehicle_type', 'tonnage', 'category', 'transport_type', 'name_q', 'nomenclature_q')


class NomenclatureTireFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.NomenclatureTire
        fields = ('id', 'name_q')


class NomenclatureBatteryFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.NomenclatureBattery
        fields = ('id', 'name_q')


class TypeFilter(django_filters.FilterSet):
    transport_type = django_filters.CharFilter(field_name='category__transport_type', lookup_expr='exact')
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Type
        fields = ('id', 'category', 'parent_type', 'transport_type', 'name_q')


class CategoryFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Category
        fields = ('id', 'transport_type', 'name_q')
