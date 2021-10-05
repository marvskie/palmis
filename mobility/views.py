import logging
from datetime import datetime

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
import xlwt
from django.db.models import Sum, F, Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from commons import consts as common_consts
from commons.models import Unit
from mobility import serializers, models, filters, permissions
from inventory.models import TransferRecord
from inventory import consts as inventory_consts
from message.models import Message
from message.views import MessageViewSet


logger = logging.getLogger(__name__)

FONT_HEADER = xlwt.easyxf('align: vert centre, horiz centre, wrap on; font: bold on')
FONT_LABEL = xlwt.easyxf('align: vert centre; font: bold on')
FONT_BODY_REG = xlwt.easyxf('align: vert centre, wrap on')
FONT_NUM_REG = xlwt.easyxf('align: vert centre;', num_format_str='#,##0.00')
FONT_BODY_NEG = xlwt.easyxf('align: vert centre; font: color-index red; align: wrap on')
FONT_NUM_NEG = xlwt.easyxf('align: vert centre; font: color-index red', num_format_str='#,##0.00')


class BatteryRecordViewSet(viewsets.GenericViewSet):
    model = TransferRecord
    queryset = TransferRecord.objects.none()
    filter_class = filters.BatteryRecordFilter

    def get_queryset(self):
        return TransferRecord.objects.\
            filter(content_type__model='nomenclaturebattery').\
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


class TireRecordViewSet(viewsets.GenericViewSet):
    model = TransferRecord
    queryset = TransferRecord.objects.none()
    filter_class = filters.TireRecordFilter

    def get_queryset(self):
        return TransferRecord.objects.\
            filter(content_type__model='nomenclaturetire').\
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


class RepairRecordViewSet(viewsets.ModelViewSet):
    model = models.RepairRecord
    queryset = models.RepairRecord.objects.none()
    filter_class = filters.RepairRecordFilter
    permission_classes = [permissions.VehicleRepairPermission]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.RepairRecordSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return serializers.RepairRecordCUSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    def get_queryset(self):
        user = self.request.user
        account = user.account.account_dict()

        if common_consts.is_og4(account['organization']):
            return models.RepairRecord.objects.all().order_by('-requested_on')
        elif account['organization'] == common_consts.PAMU:
            return models.RepairRecord.objects.filter(vehicle__unit__pamu_id=account['division']).\
                order_by('-requested_on')
        return models.RepairRecord.objects.none()


class VehicleRecordViewSet(viewsets.ModelViewSet):
    model = models.VehicleRecord
    queryset = models.VehicleRecord.objects.none()
    filter_class = filters.VehicleRecordFilter
    permission_classes = [permissions.VehiclePermission]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.VehicleRecordListSerializer
        elif self.action == 'retrieve':
            return serializers.VehicleRecordRetrieveSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            user = self.request.user
            account = user.account.account_dict()

            if common_consts.is_og4(account['organization']):
                return serializers.VehicleRecordMbCUSerializer
            elif account['organization'] == common_consts.PAMU:
                return serializers.VehicleRecordPamuUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        account = user.account.account_dict()

        if common_consts.is_og4(account['organization']):
            return models.VehicleRecord.objects.all().order_by('item_code')
        elif account['organization'] == common_consts.PAMU:
            return models.VehicleRecord.objects.filter(unit__pamu=account['division']).order_by('item_code')
        return models.VehicleRecord.objects.none()


class NomenclatureViewSet(viewsets.ModelViewSet):
    model = models.NomenclatureVehicle
    queryset = models.NomenclatureVehicle.objects.all()
    filter_class = filters.NomenclatureFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.NomenclatureSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return serializers.NomenclatureCUSerializer


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Type
    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer
    filter_class = filters.TypeFilter


class TonnageViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Tonnage
    queryset = models.Tonnage.objects.all()
    serializer_class = serializers.TonnageSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Category
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_class = filters.CategoryFilter


class NomenclatureTireViewSet(viewsets.ModelViewSet):
    model = models.NomenclatureTire
    queryset = models.NomenclatureTire.objects.all().order_by('id')
    serializer_class = serializers.NomenclatureTireSerializer
    filter_class = filters.NomenclatureTireFilter


class NomenclatureBatteryViewSet(viewsets.ModelViewSet):
    model = models.NomenclatureBattery
    queryset = models.NomenclatureBattery.objects.all()
    serializer_class = serializers.NomenclatureBatterySerializer
    filter_class = filters.NomenclatureBatteryFilter


class VehicleRemarksViewSet(MessageViewSet):
    permission_classes = [permissions.RemarksPermission]

    def get_object_id(self):
        return self.request.data.get('vehicle_record') or self.request.query_params.get('vehicle_record')

    def get_content_type(self):
        return ContentType.objects.get(model='vehiclerecord').id

    def get_pamu_queryset(self):
        user = self.request.user
        account = user.account.account_dict()
        return Message.objects.filter(content_type_id=self.get_content_type(),
                                      vehicle_record__unit__pamu_id=account['division'])


@api_view(['GET'])
def get_transport_type(request):
    data = []

    for code, name in models.TRANSPORT_TYPES:
        data.append({'code': code, 'name': name})

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_repair_implementation(request):
    data = []

    for code, name in models.REPAIR_IMPLEMENTATION:
        data.append({'code': code, 'name': name})

    return Response(data=data, status=status.HTTP_200_OK)


def convert_date_readable(date_str: str, empty='-'):
    """
    Converts date string of the format YYYY-MM-DD to DD-MMM YYYY
    :param date_str: Date string of the format YYYY-MM-DD
    :return: Date string of the format DD-MMM YYYY
    """
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d-%b %Y')
    return empty


@api_view(['POST'])
@permission_classes([permissions.ReportsPermission])
def export_repair(request):
    data = request.data
    account = request.user.account.account_dict()

    requested_on_start = data.get('requested_on_start')
    requested_on_end = data.get('requested_on_end')

    if not (requested_on_start and requested_on_end):
        return Response({'data': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    if datetime.strptime(requested_on_start, '%Y-%m-%d') > datetime.strptime(requested_on_end, '%Y-%m-%d'):
        return Response({'data': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    records = models.RepairRecord.objects.filter(requested_on__range=(requested_on_start, requested_on_end))

    item_code = data.get('item_code')
    unit_pk = data.get('unit')
    pamu_pk = data.get('pamu')
    has_fur = data.get('has_fur')

    period = f'{convert_date_readable(requested_on_start)} to {convert_date_readable(requested_on_end)}'
    units = ''
    has_fur_str = 'None'

    if has_fur is None:
        has_fur_str = ''
    elif has_fur:
        has_fur_str = 'Submitted'

    if item_code:
        item_code = item_code.strip()
        records = records.filter(vehicle__item_code__iexact=item_code)

    if common_consts.is_og4(account['organization']):
        if unit_pk:
            records = records.filter(vehicle__unit_id__in=unit_pk).distinct()
            units = ', '.join(Unit.objects.filter(pk__in=unit_pk).values_list('name', flat=True))

        if pamu_pk:
            records = records.filter(vehicle__unit__pamu_id__in=pamu_pk)
            units = ', '.join(Unit.objects.filter(pamu_id__in=pamu_pk).values_list('name', flat=True))
    elif account['organization'] == common_consts.PAMU:
        if unit_pk:
            units = Unit.objects.filter(pk__in=unit_pk, pamu_pk=account['division'])
            records = records.filter(vehicle__unit__in=units)
            units = ', '.join(units.values_list('name', flat=True))
        else:
            records = records.filter(vehicle__unit__pamu_id=account['division'])
            units = ', '.join(Unit.objects.filter(pamu_id=account['division']).values_list('name', flat=True))

    if has_fur is not None:
        records = records.filter(has_fur=has_fur)

    records = records.distinct()

    response = HttpResponse(content_type='application/ms-excel')
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('Sheet 1')

    now = datetime.now().date().strftime('%d-%b %Y')
    title = f'STATUS OF FUNDED REPAIRS as of {now}'

    headers = [
        ('', 4),
        ('Item Code', 10),
        ('Nomenclature', 35),
        ('Plate No', 10),
        ('Engine No', 15),
        ('Chassis No', 15),
        ('Requested On', 12),
        ('Completed On', 12),
        ('ASA No', 14),
        ('RRF No', 14),
        ('End User', 10),
        ('Implementation', 14),
        ('Amount', 13),
        ('Has FUR', 10)
    ]
    length = len(headers) - 1

    row = 0
    sheet.write_merge(row, row, 0, length, title, FONT_HEADER)
    row += 1

    sheet.write_merge(row, row, 0, 1, 'Period', FONT_LABEL)
    sheet.write_merge(row, row, 2, length, period, FONT_BODY_REG)
    row += 1
    sheet.write_merge(row, row, 0, 1, 'Unit', FONT_LABEL)
    sheet.write_merge(row, row, 2, length, units, FONT_BODY_REG)
    row += 1
    sheet.write_merge(row, row, 0, 1, 'Item Code', FONT_LABEL)
    sheet.write_merge(row, row, 2, length, item_code, FONT_BODY_REG)
    row += 1
    sheet.write_merge(row, row, 0, 1, 'Has FUR', FONT_LABEL)
    sheet.write_merge(row, row, 2, length, has_fur_str, FONT_BODY_REG)
    row += 2

    sheet.write_merge(row, row, 0, 5, 'Vehicle Details', FONT_HEADER)
    sheet.write_merge(row, row, 6, length, 'Repair Details', FONT_HEADER)
    row += 1

    for col, (header, width) in enumerate(headers):
        sheet.write(row, col, header, FONT_HEADER)
        sheet.col(col).width = 256 * width

    row += 1
    n = 1
    for record in records:
        sheet.write(row, 0, n, FONT_BODY_REG)
        sheet.write(row, 1, record.vehicle.item_code, FONT_BODY_REG)
        sheet.write(row, 2, record.vehicle.nomenclature.nomenclature, FONT_BODY_REG)
        sheet.write(row, 3, record.vehicle.plate_no, FONT_BODY_REG)
        sheet.write(row, 4, record.vehicle.engine_no, FONT_BODY_REG)
        sheet.write(row, 5, record.vehicle.chassis_no, FONT_BODY_REG)
        sheet.write(row, 6, convert_date_readable(str(record.requested_on)), FONT_BODY_REG)
        sheet.write(row, 7, convert_date_readable(str(record.completed_on or '')), FONT_BODY_REG)
        sheet.write(row, 8, record.advice_no, FONT_BODY_REG)
        sheet.write(row, 9, record.authority, FONT_BODY_REG)
        sheet.write(row, 10, record.unit.name, FONT_BODY_REG)
        sheet.write(row, 11, record.get_implementation_display(), FONT_BODY_REG)
        sheet.write(row, 12, record.amount_released, FONT_NUM_REG)

        has_fur = 'None'
        font = FONT_BODY_NEG
        if record.has_fur:
            has_fur = 'Submitted'
            font = FONT_BODY_REG

        sheet.write(row, 13, has_fur, font)

        row += 1
        n += 1

    response['filename'] = 'Status of Funded Repairs - Vehicle Record.xls'
    response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
    response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'

    wb.save(response)

    return response
