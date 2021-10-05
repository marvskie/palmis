import django_filters

from tosb import models
from inventory.models import TransferRecord


class IcieRecordFilter(django_filters.FilterSet):
    nomenclature_q = django_filters.CharFilter(field_name='icie__name', lookup_expr='icontains')

    class Meta:
        model = TransferRecord
        fields = ('id', 'fssu', 'nomenclature_q')


class NomenclatureIcieFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.NomenclatureIcie
        fields = ('id', 'name_q')
