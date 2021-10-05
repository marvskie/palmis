import logging
from datetime import datetime

import xlwt
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions as api_permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from commons.models import Unit
from commons import permissions as commons_permission
from engineering import models
from engineering import serializers
from engineering import filters
from engineering import permissions
from commons import consts as commons_consts
from message.models import Message
from message.views import MessageViewSet

logger = logging.getLogger(__name__)

FONT_HEADER = xlwt.easyxf('align: vert centre, horiz centre, wrap on; font: bold on')
FONT_LABEL = xlwt.easyxf('align: vert centre; font: bold on')
FONT_BODY_REG = xlwt.easyxf('align: vert centre, wrap on')
FONT_NUM_REG = xlwt.easyxf('align: vert centre;', num_format_str='#,##0.00')
FONT_BODY_NEG = xlwt.easyxf('align: vert centre; font: color-index red; align: wrap on')
FONT_NUM_NEG = xlwt.easyxf('align: vert centre; font: color-index red', num_format_str='#,##0.00')


# class BuildingRemarksViewSet(MessageViewSet):
#     permission_classes = [permissions.RemarksPermission]

#     def get_object_id(self):
#         return self.request.data.get('building') or self.request.query_params.get('building')

#     def get_content_type(self):
#         return ContentType.objects.get(model='buildingrecord').id

#     def get_pamu_queryset(self):
#         user = self.request.user
#         account = user.account.account_dict()
#         return Message.objects.filter(content_type_id=self.get_content_type(),
#                                       building__unit__pamu_id=account['division'])


# class CoProjectRemarksViewSet(MessageViewSet):
#     permission_classes = [permissions.RemarksPermission]

#     def get_object_id(self):
#         return self.request.data.get('co_project_record') or self.request.query_params.get('co_project_record')

#     def get_content_type(self):
#         return ContentType.objects.get(model='coprojectrecord').id

#     def get_pamu_queryset(self):
#         user = self.request.user
#         account = user.account.account_dict()
#         return Message.objects.filter(content_type_id=self.get_content_type(),
#                                       co_project__end_user__pamu_id=account['division'])


# class ReservationRemarksViewSet(MessageViewSet):
#     permission_classes = [commons_permission.OR(commons_permission.IsEB, commons_permission.IsOG4Readable)]

#     def get_object_id(self):
#         return self.request.data.get('reservation_record') or self.request.query_params.get('reservation_record')

#     def get_content_type(self):
#         return ContentType.objects.get(model='reservationrecord').id


# class RepairRecordViewSet(viewsets.ModelViewSet):
#     model = models.RepairRecord
#     queryset = models.RepairRecord.objects.none()
#     filter_class = filters.RepairRecordFilter
#     permission_classes = [permissions.EngineeringPermission]

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(created_by=user, updated_by=user)

#     def perform_update(self, serializer):
#         user = self.request.user
#         serializer.save(updated_by=user)

#     def get_serializer_class(self):
#         if self.action in ['list', 'retrieve']:
#             return serializers.RepairRecordSerializer
#         elif self.action in ['create', 'update', 'partial_update']:
#             return serializers.RepairRecordCUSerializer

#     def get_queryset(self):
#         user = self.request.user
#         account = user.account.account_dict()

#         if account['organization'] == commons_consts.PAMU:
#             return models.RepairRecord.objects.filter(building__pamu_id=account['division']).order_by('-requested_on')
#         elif commons_consts.is_og4(account['organization']):
#             return models.RepairRecord.objects.all().order_by('-requested_on')
#         return models.RepairRecord.objects.none()


# class BuildingCategoryViewSet(viewsets.ReadOnlyModelViewSet):
#     model = models.BuildingCategory
#     queryset = models.BuildingCategory.objects.all().order_by('order')
#     serializer_class = serializers.BuildingCategorySerializer


# class BuildingRecordViewSet(viewsets.ModelViewSet):
#     model = models.BuildingRecord
#     queryset = models.BuildingRecord.objects.none()
#     filter_class = filters.BuildingRecordFilter
#     permission_classes = [permissions.EngineeringPermission]

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(created_by=user, updated_by=user)

#     def perform_update(self, serializer):
#         user = self.request.user
#         serializer.save(updated_by=user)

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return serializers.BuildingRecordListSerializer
#         elif self.action == 'retrieve':
#             return serializers.BuildingRecordSerializer
#         elif self.action in ['create', 'update', 'partial_update']:
#             return serializers.BuildingRecordCUSerializer

#     def get_queryset(self):
#         user = self.request.user
#         account = user.account.account_dict()

#         if account['organization'] == commons_consts.PAMU:
#             return models.BuildingRecord.objects.filter(pamu_id=account['division'])
#         elif commons_consts.is_og4(account['organization']):
#             return models.BuildingRecord.objects.all()
#         return models.BuildingRecord.objects.none()


# class ReservationRecordViewSet(viewsets.ModelViewSet):
#     model = models.ReservationRecord
#     queryset = models.ReservationRecord.objects.all()
#     filter_class = filters.ReservationRecordFilter
#     permission_classes = [permissions.EngineeringPermission]

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(created_by=user, updated_by=user)

#     def perform_update(self, serializer):
#         user = self.request.user
#         serializer.save(updated_by=user)

#     def get_serializer_class(self):
#         if self.action in ['list', 'retrieve']:
#             return serializers.ReservationRecordSerializer
#         elif self.action in ['create', 'update', 'partial_update']:
#             return serializers.ReservationRecordCUSerializer


# class CoProjectRecordViewSet(viewsets.ModelViewSet):
#     model = models.CoProjectRecord
#     queryset = models.CoProjectRecord.objects.all()
#     filter_class = filters.CoProjectRecordFilter
#     permission_classes = [permissions.EngineeringPermission]

#     def perform_create(self, serializer):
#         user = self.request.user
#         serializer.save(created_by=user, updated_by=user)

#     def perform_update(self, serializer):
#         user = self.request.user
#         serializer.save(updated_by=user)

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return serializers.CoProjectRecordListSerializer
#         elif self.action == 'retrieve':
#             return serializers.CoProjectRecordSerializer
#         elif self.action in ['create', 'update', 'partial_update']:
#             return serializers.CoProjectRecordCUSerializer


# class CoStatusViewSet(viewsets.ReadOnlyModelViewSet):
#     model = models.CoStatus
#     queryset = models.CoStatus.objects.all()
#     serializer_class = serializers.CoStatusSerializer


# def convert_date_readable(date_str: str, empty='-'):
#     """
#     Converts date string of the format YYYY-MM-DD to DD-MMM YYYY
#     :param date_str: Date string of the format YYYY-MM-DD
#     :return: Date string of the format DD-MMM YYYY
#     """
#     if date_str:
#         return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d-%b %Y')
#     return empty


# @api_view(['POST'])
# @permission_classes([permissions.ReportsPermission])
# def export_repair(request):
#     data = request.data
#     account = request.user.account.account_dict()

#     requested_on_start = data.get('requested_on_start')
#     requested_on_end = data.get('requested_on_end')

#     if not (requested_on_start and requested_on_end):
#         return Response({'data': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

#     if datetime.strptime(requested_on_start, '%Y-%m-%d') > datetime.strptime(requested_on_end, '%Y-%m-%d'):
#         return Response({'data': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

#     records = models.RepairRecord.objects.filter(requested_on__range=(requested_on_start, requested_on_end))

#     item_code = data.get('building_code')
#     unit_pk = data.get('unit')
#     pamu_pk = data.get('pamu')
#     has_fur = data.get('has_fur')

#     period = f'{convert_date_readable(requested_on_start)} to {convert_date_readable(requested_on_end)}'
#     units = ''
#     has_fur_str = 'None'

#     if has_fur is None:
#         has_fur_str = ''
#     elif has_fur:
#         has_fur_str = 'Submitted'

#     if item_code:
#         item_code = item_code.strip()
#         records = records.filter(building__building_code__iexact=item_code)

#     if commons_consts.is_og4(account['organization']):
#         if unit_pk:
#             records = records.filter(building__unit_id__in=unit_pk)
#             units = ', '.join(Unit.objects.filter(pk__in=unit_pk).values_list('name', flat=True))

#         if pamu_pk:
#             records = records.filter(building__unit__pamu_id__in=pamu_pk)
#             units = ', '.join(Unit.objects.filter(pamu_id__in=pamu_pk).values_list('name', flat=True))
#     elif account['organization'] == commons_consts.PAMU:
#         if unit_pk:
#             units = Unit.objects.filter(pk__in=unit_pk, pamu_pk=account['division'])
#             records = records.filter(building__unit__in=units)
#             units = ', '.join(units.values_list('name', flat=True))
#         else:
#             records = records.filter(building__unit__pamu=account['division'])
#             units = ', '.join(Unit.objects.filter(pamu_id=account['division']).values_list('name', flat=True))

#     if has_fur is not None:
#         records = records.filter(has_fur=has_fur)

#     records = records.distinct()

#     response = HttpResponse(content_type='application/ms-excel')
#     wb = xlwt.Workbook(encoding='utf-8')
#     sheet = wb.add_sheet('Sheet 1')

#     now = datetime.now().date().strftime('%d-%b %Y')
#     title = f'STATUS OF FUNDED REPAIRS as of {now}'

#     headers = [
#         ('', 4),
#         ('Building Code', 10),
#         ('Reservation', 25),
#         ('Category', 20),
#         ('Description', 15),
#         ('Requested On', 12),
#         ('Completed On', 12),
#         ('ASA No', 14),
#         ('RRF No', 14),
#         ('End User', 10),
#         ('Amount', 13),
#         ('Has FUR', 10)
#     ]

#     length = len(headers) - 1

#     row = 0
#     sheet.write_merge(row, row, 0, length, title, FONT_HEADER)
#     row += 1

#     sheet.write_merge(row, row, 0, 1, 'Period', FONT_LABEL)
#     sheet.write_merge(row, row, 2, length, period, FONT_BODY_REG)
#     row += 1
#     sheet.write_merge(row, row, 0, 1, 'Unit', FONT_LABEL)
#     sheet.write_merge(row, row, 2, length, units, FONT_BODY_REG)
#     row += 1
#     sheet.write_merge(row, row, 0, 1, 'Building Code', FONT_LABEL)
#     sheet.write_merge(row, row, 2, length, item_code, FONT_BODY_REG)
#     row += 1
#     sheet.write_merge(row, row, 0, 1, 'Has FUR', FONT_LABEL)
#     sheet.write_merge(row, row, 2, length, has_fur_str, FONT_BODY_REG)
#     row += 2

#     sheet.write_merge(row, row, 0, 5, 'Facility Details', FONT_HEADER)
#     sheet.write_merge(row, row, 6, length, 'Repair Details', FONT_HEADER)
#     row += 1

#     for col, (header, width) in enumerate(headers):
#         sheet.write(row, col, header, FONT_HEADER)
#         sheet.col(col).width = 256 * width

#     row += 1
#     n = 1
#     for record in records:
#         sheet.write(row, 0, n, FONT_BODY_REG)
#         sheet.write(row, 1, record.building.building_code, FONT_BODY_REG)
#         sheet.write(row, 2, record.building.reservation.name, FONT_BODY_REG)
#         sheet.write(row, 3, record.building.category.name, FONT_BODY_REG)
#         sheet.write(row, 4, record.building.description, FONT_BODY_REG)
#         sheet.write(row, 5, convert_date_readable(str(record.requested_on)), FONT_BODY_REG)
#         sheet.write(row, 6, convert_date_readable(str(record.completed_on or '')), FONT_BODY_REG)
#         sheet.write(row, 7, record.advice_no, FONT_BODY_REG)
#         sheet.write(row, 8, record.authority, FONT_BODY_REG)
#         sheet.write(row, 9, record.unit.name, FONT_BODY_REG)
#         sheet.write(row, 10, record.amount_released, FONT_NUM_REG)

#         has_fur = 'None'
#         font = FONT_BODY_NEG
#         if record.has_fur:
#             has_fur = 'Submitted'
#             font = FONT_BODY_REG

#         sheet.write(row, 11, has_fur, font)

#         row += 1
#         n += 1

#     response['filename'] = 'Status of Funded Repairs - Facility Record.xls'
#     response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
#     response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'

#     wb.save(response)

#     return response


# @api_view(['POST'])
# @permission_classes([permissions.ReportsPermission])
# def export_co(request):
#     data = request.data
#     account = request.user.account.account_dict()

#     start_construction_start = data.get('start_construction_start')
#     start_construction_end = data.get('start_construction_end')

#     if not (start_construction_start and start_construction_end):
#         return Response({'data': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

#     if datetime.strptime(start_construction_start, '%Y-%m-%d') > datetime.strptime(start_construction_end, '%Y-%m-%d'):
#         return Response({'data': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

#     records = models.CoProjectRecord.objects.filter(
#         start_construction__range=(start_construction_start, start_construction_end))

#     contractor = data.get('contractor') or ''
#     unit_pk = data.get('unit')
#     status_pk = data.get('status')

#     period = f'{convert_date_readable(start_construction_start)} to {convert_date_readable(start_construction_end)}'
#     units = ''
#     statuses = ''

#     if contractor:
#         contractor = contractor.strip()
#         records = records.filter(contractor__icontains=contractor)

#     if status_pk:
#         records = records.filter(status_pk__in=status_pk)
#         statuses = ', '.join(models.CoStatus.objects.fitler(pk__in=status_pk).values_list('name', flat=True))

#     if commons_consts.is_og4(account['organization']):
#         if unit_pk:
#             records = records.filter(end_user_id__in=unit_pk)
#             units = ', '.join(Unit.objects.filter(pk__in=unit_pk).values_list('name', flat=True))
#     elif account['organization'] == commons_consts.PAMU:
#         if unit_pk:
#             units = Unit.objects.filter(pk__in=unit_pk, pamu_pk=account['division'])
#             records = records.filter(end_user__in=units)
#             units = ', '.join(units.values_list('name', flat=True))
#         else:
#             records = records.filter(end_user__pamu=account['division'])
#             units = ', '.join(Unit.objects.filter(pamu_id=account['division']).values_list('name', flat=True))

#     response = HttpResponse(content_type='application/ms-excel')
#     wb = xlwt.Workbook(encoding='utf-8')
#     sheet = wb.add_sheet('Sheet 1')

#     now = datetime.now().date().strftime('%d-%b %Y')
#     title = f'STATUS OF CAPITAL OUTLAY FUNDED PROJECTS as of {now}'

#     headers = [
#         ('', 4),
#         ('Project Name', 30),
#         ('End User', 10),
#         ('Original Cost', 13),
#         ('ABC', 13),
#         ('Bid Amount', 13),
#         ('Bid Residual', 13),
#         ('Object Code', 13),
#         ('Contractor', 20),
#         ('Start of Construction', 13),
#         ('Target Completion', 13),
#         ('Actual Completion', 13),
#         ('Status', 10),
#         ('Physical Accomplishment', 15),
#         ('Remarks', 30)
#     ]
#     length = len(headers) - 1

#     row = 0
#     sheet.write_merge(row, row, 0, length, title, FONT_HEADER)
#     row += 1

#     sheet.write_merge(row, row, 0, 1, 'Period', FONT_LABEL)
#     sheet.write_merge(row, row, 2, length, period, FONT_BODY_REG)
#     row += 1
#     sheet.write_merge(row, row, 0, 1, 'Unit', FONT_LABEL)
#     sheet.write_merge(row, row, 2, length, units, FONT_BODY_REG)
#     row += 1
#     sheet.write_merge(row, row, 0, 1, 'Status', FONT_LABEL)
#     sheet.write_merge(row, row, 2, length, statuses, FONT_BODY_REG)
#     row += 1
#     sheet.write_merge(row, row, 0, 1, 'Contractor', FONT_LABEL)
#     sheet.write_merge(row, row, 2, length, contractor, FONT_BODY_REG)
#     row += 2

#     for col, (header, width) in enumerate(headers):
#         sheet.write(row, col, header, FONT_HEADER)
#         sheet.col(col).width = 256 * width

#     row += 1
#     n = 1
#     for record in records:
#         sheet.write(row, 0, n, FONT_BODY_REG)
#         sheet.write(row, 1, record.project_name, FONT_BODY_REG)
#         sheet.write(row, 2, record.end_user.name, FONT_BODY_REG)
#         sheet.write(row, 3, record.original_cost, FONT_NUM_REG)
#         sheet.write(row, 4, record.approved_budget, FONT_NUM_REG)
#         sheet.write(row, 5, record.bid_amount, FONT_NUM_REG)
#         sheet.write(row, 6, xlwt.Formula(f'E{row + 1}+F{row + 1}'), FONT_NUM_REG)
#         sheet.write(row, 7, record.object_code.code, FONT_BODY_REG)
#         sheet.write(row, 8, record.contractor, FONT_BODY_REG)
#         sheet.write(row, 9, convert_date_readable(str(record.start_construction or '')), FONT_BODY_REG)
#         sheet.write(row, 10, convert_date_readable(str(record.target_completion or '')), FONT_BODY_REG)
#         sheet.write(row, 11, convert_date_readable(str(record.actual_completion or '')), FONT_BODY_REG)
#         sheet.write(row, 12, record.status.name, FONT_BODY_REG)

#         row += 1
#         n += 1

#     response['filename'] = 'Status of Capital Outlay Funded Projects.xls'
#     response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
#     response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'

#     wb.save(response)

#     return response


# @api_view(['GET'])
# def export_facility(request, pk):
#     pass


# @api_view(['GET'])
# def export_facility_list(request):
#     facilities = models.BuildingRecord.objects.order_by('reservation', 'building_code')

#     wb = xlwt.Workbook(encoding='utf-8')
#     sheet = wb.add_sheet('Sheet 1')

#     headers = ['Reservation', 'Building Code', 'Category', 'Unit', 'Description']
#     widths = [35, 12, 20, 15, 35]
#     cols = len(headers)
#     row = 0

#     sheet.write_merge(row, row, 0, cols - 1, 'Facility Records', FONT_HEADER)

#     row += 2
#     for i, header in enumerate(headers):
#         sheet.write(row, i, header, FONT_LABEL)
#         sheet.col(i).width = 256 * widths[i]

#     row += 1
#     for facility in facilities:
#         sheet.write(row, 0, facility.reservation.name, FONT_BODY_REG)
#         sheet.write(row, 1, facility.building_code, FONT_BODY_REG)
#         sheet.write(row, 2, facility.category.name, FONT_BODY_REG)
#         sheet.write(row, 3, facility.unit.name, FONT_BODY_REG)
#         sheet.write(row, 4, facility.description, FONT_BODY_REG)
#         row += 1

#     title = 'Facility Records'
#     response = HttpResponse(content_type='application/ms-excel')
#     response['filename'] = f'{title}.xls'
#     response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
#     response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'
#     wb.save(response)

#     return response


# @api_view(['GET'])
# def export_co_list(request):
#     cos = models.CoProjectRecord.objects.order_by('project_name')

#     wb = xlwt.Workbook(encoding='utf-8')
#     sheet = wb.add_sheet('Sheet 1')

#     headers = ['Project Name', 'End User', 'Object Code', 'Status', 'Original Cost', 'ABC', 'Bid Amount',
#                'Bid Residual', 'Contractor', 'Start of Construction', 'Target Completion', 'Actual Completion']
#     widths = [30, 15, 15, 20, 15, 15, 15, 15, 15, 20, 20, 20]
#     cols = len(headers)
#     row = 0

#     sheet.write_merge(row, row, 0, cols - 1, 'Capital Outlay Funded Project Records', FONT_HEADER)

#     row += 2
#     for i, header in enumerate(headers):
#         sheet.write(row, i, header, FONT_LABEL)
#         sheet.col(i).width = 256 * widths[i]

#     row += 1
#     for co in cos:
#         sheet.write(row, 0, co.project_name, FONT_BODY_REG)
#         sheet.write(row, 1, co.end_user.name, FONT_BODY_REG)
#         sheet.write(row, 2, co.object_code.code, FONT_BODY_REG)
#         sheet.write(row, 3, co.status.name, FONT_BODY_REG)
#         sheet.write(row, 4, co.original_cost, FONT_NUM_REG)
#         sheet.write(row, 5, co.approved_budget, FONT_NUM_REG)
#         sheet.write(row, 6, co.bid_amount, FONT_NUM_REG)
#         sheet.write(row, 7, co.bid_residual(), FONT_NUM_REG)
#         sheet.write(row, 8, co.contractor, FONT_BODY_REG)
#         sheet.write(row, 9, str(co.start_construction), FONT_BODY_REG)
#         sheet.write(row, 10, str(co.target_completion), FONT_BODY_REG)
#         sheet.write(row, 11, str(co.actual_completion), FONT_BODY_REG)
#         row += 1

#     title = 'CO Funded Project Records'
#     response = HttpResponse(content_type='application/ms-excel')
#     response['filename'] = f'{title}.xls'
#     response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
#     response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'
#     wb.save(response)

#     return response


# @api_view(['GET'])
# def export_reservation(request, pk):
#     pass


# @api_view(['GET'])
# def export_reservation_list(request):
#     reservations = models.ReservationRecord.objects.order_by('code')

#     wb = xlwt.Workbook(encoding='utf-8')
#     sheet = wb.add_sheet('Sheet 1')

#     headers = ['Code', 'Name', 'Location', 'Region', 'Lot Area (ha)', 'Camp Administrator']
#     widths = [12, 35, 20, 15, 15, 20]
#     cols = len(headers)
#     row = 0

#     sheet.write_merge(row, row, 0, cols - 1, 'Army Reservation Records', FONT_HEADER)

#     row += 2
#     for i, header in enumerate(headers):
#         sheet.write(row, i, header, FONT_LABEL)
#         sheet.col(i).width = 256 * widths[i]

#     row += 1
#     for reservation in reservations:
#         sheet.write(row, 0, reservation.code, FONT_BODY_REG)
#         sheet.write(row, 1, reservation.name, FONT_BODY_REG)
#         sheet.write(row, 2, reservation.location, FONT_BODY_REG)
#         sheet.write(row, 3, reservation.region.name, FONT_BODY_REG)
#         sheet.write(row, 4, reservation.lot_area, FONT_NUM_REG)
#         sheet.write(row, 5, reservation.camp_administrator, FONT_BODY_REG)
#         row += 1

#     title = 'Army Reservation Records'
#     response = HttpResponse(content_type='application/ms-excel')
#     response['filename'] = f'{title}.xls'
#     response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
#     response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'
#     wb.save(response)

#     return response



# ======== NEW PALMIS views

class HeavyEquipmentViewSet(viewsets.ModelViewSet):
    queryset = models.HeavyEquipment.objects.all()
    serializer_class = serializers.HeavyEquipmentSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class LightEquipmentViewSet(viewsets.ModelViewSet):
    queryset = models.LightEquipment.objects.all()
    serializer_class = serializers.LightEquipmentSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class LightRecordViewSet(viewsets.ModelViewSet):
    queryset = models.LightRecord.objects.all()
    serializer_class = serializers.LightRecordSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class WaterRecordViewSet(viewsets.ModelViewSet):
    queryset = models.WaterRecord.objects.all()
    serializer_class = serializers.WaterRecordSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class InsuranceOfBuildingViewSet(viewsets.ModelViewSet):
    queryset = models.InsuranceOfBuilding.objects.all()
    serializer_class = serializers.InsuranceOfBuildingSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class SurveyTitlingFencingViewSet(viewsets.ModelViewSet):
    queryset = models.SurveyTitlingFencing.objects.all()
    serializer_class = serializers.SurveyTitlingFencingSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class LotRentalViewSet(viewsets.ModelViewSet):
    queryset = models.LotRental.objects.all()
    serializer_class = serializers.LotRentalSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class DetailedArchitecturalAndEngineeringDesignViewSet(viewsets.ModelViewSet):
    queryset = models.DetailedArchitecturalAndEngineeringDesign.objects.all()
    serializer_class = serializers.DetailedArchitecturalAndEngineeringDesignSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ComprehensiveMasterDevelopmentPlanViewSet(viewsets.ModelViewSet):
    queryset = models.ComprehensiveMasterDevelopmentPlan.objects.all()
    serializer_class = serializers.ComprehensiveMasterDevelopmentPlanSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class CapitalOutlayViewSet(viewsets.ModelViewSet):
    queryset = models.CapitalOutlay.objects.all()
    serializer_class = serializers.CapitalOutlaySerializer
    permission_classes = [api_permissions.IsAuthenticated]

class InteragencyTransferFundViewSet(viewsets.ModelViewSet):
    queryset = models.InteragencyTransferFund.objects.all()
    serializer_class = serializers.InteragencyTransferFundSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class BasesConversionAndDevelopmentAuthorityViewSet(viewsets.ModelViewSet):
    queryset = models.BasesConversionAndDevelopmentAuthority.objects.all()
    serializer_class = serializers.BasesConversionAndDevelopmentAuthoritySerializer
    permission_classes = [api_permissions.IsAuthenticated]

class IncomingCommunicationViewSet(viewsets.ModelViewSet):
    queryset = models.IncomingCommunication.objects.all()
    serializer_class = serializers.IncomingCommunicationSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class OutgoingCommunicationViewSet(viewsets.ModelViewSet):
    queryset = models.OutgoingCommunication.objects.all()
    serializer_class = serializers.OutgoingCommunicationSerializer
    permission_classes = [api_permissions.IsAuthenticated]