import django_filters

from message.models import Message


class MessageFilter(django_filters.FilterSet):
    remarks_q = django_filters.CharFilter(field_name='remarks', lookup_expr='icontains')
    model = django_filters.CharFilter(field_name='content_type__model')

    class Meta:
        model = Message
        fields = ('id', 'model', 'remarks_q', 'object_id')
