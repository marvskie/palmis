import django_filters

from commons import models


class UnitFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = models.Unit
        fields = ('id', 'pamu', 'name_q')


class AccountFilter(django_filters.FilterSet):
    name_q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    username_q = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    organization = django_filters.NumberFilter(field_name='role__organization_id')

    class Meta:
        model = models.Account
        fields = ('id', 'active', 'organization', 'name_q', 'username_q', 'pamu', 'fssu')
