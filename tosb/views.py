import logging

from django.db.models import Sum, F, Q
from rest_framework import viewsets
from rest_framework.response import Response

from tosb import models, serializers, filters
from inventory.models import TransferRecord
from inventory import consts as inventory_consts


logger = logging.getLogger(__name__)


class IcieRecordViewSet(viewsets.GenericViewSet):
    model = TransferRecord
    queryset = TransferRecord.objects.none()
    filter_class = filters.IcieRecordFilter

    def get_queryset(self):
        return TransferRecord.objects.\
            filter(content_type__model='nomenclatureicie').\
            values('content_type', 'object_id', 'fssu').\
            annotate(
                stock_in=Sum('quantity', filter=(Q(transfer_type__code=inventory_consts.REPLENISHMENT) |
                                                 Q(transfer_type__code=inventory_consts.TRANSFER_IN))),
                stock_out=Sum('quantity', filter=(Q(transfer_type__code=inventory_consts.DISPOSE) |
                                                  Q(transfer_type__code=inventory_consts.TRANSFER_OUT))),
                fssu_name=F('fssu__name')
            ).values('content_type', 'object_id', 'fssu_name', 'stock_in', 'stock_out', 'fssu_id')

    def _serialize(self, queryset):
        data = []

        for item in queryset:
            obj = TransferRecord.objects.filter(
                content_type=item['content_type'], object_id=item['object_id']).first().content_object
            stock = (item['stock_in'] or 0) - (item['stock_out'] or 0)
            fssu = {'id': item['fssu_id'], 'name': item['fssu_name']}
            nomenclature = {'id': obj.id, 'name': obj.name}
            data.append({'nomenclature': nomenclature, 'stock': stock, 'fssu': fssu})
        return data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serialized = self._serialize(page)
            return self.get_paginated_response(serialized)

        serialized = self._serialize(queryset)
        return Response(serialized)


class NomenclatureIcieViewSet(viewsets.ModelViewSet):
    model = models.NomenclatureIcie
    queryset = models.NomenclatureIcie.objects.all()
    serializer_class = serializers.NomenclatureIcieSerializer
    filter_class = filters.NomenclatureIcieFilter
