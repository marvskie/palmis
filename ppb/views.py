import logging
from datetime import datetime

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.http import HttpResponse
from django.db.models import F
import xlwt

from commons import permissions
from commons import consts as common_consts
from ppb import filters
from ppb.models import ExpenseClass, ObjectCode, MissionArea, Dpg, ProgramObjective, Kma, MajorPap, SubPap, \
    SuggestedPap, PawafItem, Pawaf, StrategicObjective, PbdgObjective, StrategicProgram, PawafItemView, \
    PawafItemEndUser, FundRelease, FundReleaseItem, PawafItemBudgetBreakdown, FundReleaseRecipient, Status, \
    FundReleaseAsa, KeyProgram
import ppb.serializers
from ppb.permissions import PawafPermission
from ppb.documents.rrf import create
from ppb.documents.fund_utilization import compose_fund_monitoring
from ppb.documents.others import compose_summary_of_release, compose_apb_monitor, compose_budget_summary
from commons.models import Pamu, Unit

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
logger = logging.getLogger(__name__)

FONT_HEADER = xlwt.easyxf('align: vert centre, horiz centre, wrap on; font: bold on')
FONT_LABEL = xlwt.easyxf('align: vert centre; font: bold on')
FONT_BODY_REG = xlwt.easyxf('align: vert centre, wrap on')
FONT_NUM_REG = xlwt.easyxf('align: vert centre', num_format_str='#,##0.00')
FONT_BODY_NEG = xlwt.easyxf('font: color-index red; align: wrap on')
FONT_NUM_NEG = xlwt.easyxf('font: color-index red; align: vert centre', num_format_str='#,##0.00')
FONT_NUM_REG_TOTAL = xlwt.easyxf('align: vert centre; font: bold on', num_format_str='#,##0.00')
FONT_NUM_NEG_TOTAL = xlwt.easyxf('font: color-index red; font: bold on; align: vert centre;', num_format_str='#,##0.00')

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """
    def enforce_csrf(self, request):
        return

class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    model = Status
    queryset = Status.objects.all().order_by('-order')
    serializer_class = ppb.serializers.StatusSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


class ExpenseClassViewSet(viewsets.ReadOnlyModelViewSet):
    model = ExpenseClass
    queryset = ExpenseClass.objects.all()
    serializer_class = ppb.serializers.ExpenseClassSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

class ObjectCodeViewSet(viewsets.ReadOnlyModelViewSet):
    model = ObjectCode
    queryset = ObjectCode.objects.all().order_by('code')
    serializer_class = ppb.serializers.ObjectCodeSerializer
    filter_class = filters.ObjectCodeFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

class MissionAreaViewSet(viewsets.ReadOnlyModelViewSet):
    model = MissionArea
    queryset = MissionArea.objects.all()
    serializer_class = ppb.serializers.MissionAreaSerializer
    filter_class = filters.MissionAreaFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

class KeyProgramViewSet(viewsets.ReadOnlyModelViewSet):
    model = KeyProgram
    queryset = KeyProgram.objects.all().order_by('-order')
    serializer_class = ppb.serializers.KeyProgramSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

class StrategicObjectiveViewSet(viewsets.ReadOnlyModelViewSet):
    model = StrategicObjective
    queryset = StrategicObjective.objects.all()
    serializer_class = ppb.serializers.StrategicObjectiveSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

class StrategicProgramViewSet(viewsets.ReadOnlyModelViewSet):
    model = StrategicProgram
    queryset = StrategicProgram.objects.all().order_by('id')
    serializer_class = ppb.serializers.StrategicProgramSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

class PbdgObjectiveViewSet(viewsets.ReadOnlyModelViewSet):
    model = PbdgObjective
    queryset = PbdgObjective.objects.all()
    serializer_class = ppb.serializers.PbdgObjectiveSerializer
    filter_class = filters.PbdgObjectiveFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

class DpgViewSet(viewsets.ReadOnlyModelViewSet):
    model = Dpg
    queryset = Dpg.objects.filter(active=True)
    serializer_class = ppb.serializers.DpgSerializer
    permission_classes = [permissions.OR(permissions.IsPPB, permissions.IsExecutiveReadable)]
    filter_class = filters.DpgFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



class ProgramObjectiveViewSet(viewsets.ReadOnlyModelViewSet):
    model = ProgramObjective
    queryset = ProgramObjective.objects.filter(dpg__active=True)
    serializer_class = ppb.serializers.ProgramObjectiveSerializer
    permission_classes = [permissions.OR(permissions.IsPPB, permissions.IsExecutiveReadable)]
    filter_class = filters.ProgramObjectiveFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



class KmaViewSet(viewsets.ReadOnlyModelViewSet):
    model = Kma
    queryset = Kma.objects.all()
    serializer_class = ppb.serializers.KmaSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



class MajorPapViewSet(viewsets.ReadOnlyModelViewSet):
    model = MajorPap
    queryset = MajorPap.objects.all().order_by('name')
    serializer_class = ppb.serializers.MajorPapSerializer
    filter_class = filters.MajorPapFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



class SubPapViewSet(viewsets.ReadOnlyModelViewSet):
    models = SubPap
    queryset = SubPap.objects.all().order_by('name')
    serializer_class = ppb.serializers.SubPapSerializer
    filter_class = filters.SubPapFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



class SuggestedPapViewSet(viewsets.ReadOnlyModelViewSet):
    model = SuggestedPap
    queryset = SuggestedPap.objects.all().order_by('name')
    serializer_class = ppb.serializers.SuggestedPapSerializer
    filter_class = filters.SuggestedPapFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



class FundReleaseViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                         mixins.ListModelMixin, mixins.RetrieveModelMixin):
    model = FundRelease
    queryset = FundRelease.objects.all().order_by('-serial')
    permission_classes = [permissions.IsPPB]
    filter_class = filters.FundReleaseFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ppb.serializers.FundReleaseCUSerializer
        elif self.action == 'list':
            return ppb.serializers.FundReleaseListSerializer
        else:
            return ppb.serializers.FundReleaseRetrieveSerializer

    def create(self, request, *args, **kwargs):
        request.data['date'] = datetime.today().date()
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    def get_queryset(self):
        user = self.request.user
        account = user.account

        if account.special_permissions and 'can_rrf_cmd' in account.special_permissions.get('ppb', []):
            return super().get_queryset()

        return super().get_queryset().filter(cmd=False)


class FundReleaseItemViewSet(viewsets.ModelViewSet):
    model = FundReleaseItem
    queryset = FundReleaseItem.objects.all().order_by('object_code__code', 'specific_purpose')
    permission_classes = []
    filter_class = filters.FundReleaseItemFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ppb.serializers.FundReleaseItemCUSerializer
        return ppb.serializers.FundReleaseItemRetrieveSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        user = self.request.user
        fund_release = instance.fund_release
        fund_release.updated_by = user
        fund_release.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        user = self.request.user
        fund_release = instance.fund_release
        fund_release.updated_by = user
        fund_release.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.release_recipients.all().delete()

        self.perform_destroy(instance)

        user = self.request.user
        fund_release = instance.fund_release
        fund_release.updated_by = user
        fund_release.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        user = self.request.user
        account = user.account
        if account.special_permissions and 'can_rrf_cmd' in account.special_permissions.get('ppb', []):
            return super().get_queryset()
        return super().get_queryset().filter(fund_release__cmd=False)


class FundReleaseAsaViewSet(viewsets.ModelViewSet):
    model = FundReleaseAsa
    queryset = FundReleaseAsa.objects.all()
    permission_classes = []
    filter_class = filters.FundReleaseAsaFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ppb.serializers.FundReleaseAsaCUSerializer
        elif self.action == 'list':
            return ppb.serializers.FundReleaseAsaListSerializer
        return ppb.serializers.FundReleaseAsaRetrieveSerializer

class PawafViewSet(viewsets.ModelViewSet):
    model = Pawaf
    queryset = Pawaf.objects.none()
    permission_classes = []
    filter_class = filters.PawafFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ppb.serializers.PawafCUSerializer
        return ppb.serializers.PawafSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        items = data.pop('pawaf_items', None) or {}

        to_delete_items = set()
        for delete_item in items.get('to_delete') or []:
            for _, value in delete_item.items():
                to_delete_items.add(value)

        to_add_items = items.get('to_add') or []
        to_update_items = items.get('to_update') or []

        if to_add_items:
            data['pawaf_items'] = to_add_items

        context = self.get_serializer_context()
        context['pawaf_items'] = {
            'to_delete': to_delete_items,
            'to_update': to_update_items
        }
        instance = self.get_object()
        context['pawaf'] = instance

        partial = kwargs.pop('partial', False)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=partial, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def get_queryset(self):
        return Pawaf.objects.all()

class PawafItemViewSet(viewsets.ModelViewSet):
    model = PawafItem
    queryset = PawafItem.objects.none()
    filter_class = filters.PawafItemFilter
    permission_classes = []
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ppb.serializers.PawafItemCUSerializer
        return ppb.serializers.PawafItemSerializer

    def list(self, request, *args, **kwargs):
        view_by = request.query_params.get('view_by') or 0

        try:
            view_obj = PawafItemView.objects.get(pk=view_by)
        except PawafItemView.DoesNotExist:
            return super().list(request, *args, **kwargs)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = view_obj.get_view(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(queryset)

        return Response(data=queryset)

    def get_queryset(self):
        user = self.request.user
        account = user.account.account_dict()
        qs = PawafItem.objects.all().order_by(
                'strategic_program', 'suggested_pap__sub_pap__major_pap', 'suggested_pap', 'id')

        if account['organization'] == common_consts.PPB:
            return qs
        return qs.filter(branch__iexact=account['organization'])


class PawafItemViewViewSet(viewsets.ReadOnlyModelViewSet):
    model = PawafItemView
    queryset = PawafItemView.objects.all().order_by('order')
    serializer_class = ppb.serializers.PawafItemViewSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



class PawafItemEndUserViewSet(viewsets.ReadOnlyModelViewSet):
    model = PawafItemEndUser
    queryset = PawafItemEndUser.objects.all()
    serializer_class = ppb.serializers.PawafItemEndUserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



class PawaItemBudgetBreakdownForRrfSelectionViewSet(viewsets.ReadOnlyModelViewSet):
    model = PawafItemBudgetBreakdown
    queryset = PawafItemBudgetBreakdown.objects.all().order_by('pawaf_item__specific_pap', 'object_code__code')
    serializer_class = ppb.serializers.PawafItemBudgetBreakdownForRrfSelectionSerializer
    filter_class = filters.PawafItemBudgetBreakdownFilter
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)



@api_view(['GET'])
@permission_classes([])
def get_programs(request):
    params = request.query_params

    data = [{'code': code, 'display': display} for code, display in MajorPap.PA_SUB_PROGRAM_CHOICES]

    if params.get('fund_release'):
        try:
            fund_release = FundRelease.objects.get(pk=params['fund_release'])
            choices = fund_release.specific_paps.all(). \
                values_list('suggested_pap__sub_pap__major_pap__pa_sub_program', flat=True). \
                distinct('suggested_pap__sub_pap__major_pap__pa_sub_program')

            data = [{'code': code, 'display': display} for code, display in MajorPap.PA_SUB_PROGRAM_CHOICES if
                    code in choices]
        except FundRelease.DoesNotExist:
            pass

    return Response(data={'results': data}, headers={'Content-Type': 'application/json'})


@api_view(['GET'])
@permission_classes([])
def download_budget_summary(request, pk):
    user = request.user
    account = user.account.account_dict()

    try:
        budget = Pawaf.objects.get(pk=pk)
    except Pawaf.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, headers={'Content-Type': 'application/json'})

    data = request.data
    filters = {}

    if data.get('branch') or account['organization'] != common_consts.PPB:
        filters['branch__iexact'] = data.get('branch', '').strip() or account['organization']
    if data.get('end_user'):
        filters['end_user'] = data['end_user']
    if data.get('specific_pap'):
        filters['specific_pap__icontains'] = data['specific_pap']

    budget_items = budget.pawaf_items.all().order_by(
        'branch', 'suggested_pap__sub_pap__major_pap__name', 'specific_pap', 'end_user__name')

    if filters:
        budget_items = budget.pawaf_items.filter(**filters)

    response = HttpResponse(content_type='application/ms-excel')

    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('Sheet 1')
    compose_budget_summary(budget, budget_items, sheet)

    title = f'{budget.description} Budget Summary'
    response['filename'] = f'{title}.xls'
    response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
    response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'
    wb.save(response)

    return response


@api_view(['GET'])
@permission_classes([])
def download_apb_monitor(request, pk):
    try:
        budget = Pawaf.objects.get(pk=pk)
    except Pawaf.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, headers={'Content-Type': 'application/json'})

    response = HttpResponse(content_type='application/ms-excel')

    wb = xlwt.Workbook(encoding='utf-8')
    compose_apb_monitor(budget, wb)

    title = 'Budget Record'
    response['filename'] = f'{title}.xls'
    response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
    response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'
    wb.save(response)

    return response


@api_view(['GET'])
@permission_classes([])
def download_rrf(request, pk):
    try:
        rrf = FundRelease.objects.get(pk=pk)
    except FundRelease.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, headers={'Content-Type': 'application/json'})

    document = create(rrf)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    title = f'RRF {rrf.rrf_no}'
    response['filename'] = f'{title}.docx'
    response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
    document.save(response)

    return response


@api_view(['GET'])
@permission_classes([])
def download_summary_of_release(request):
    budget = request.GET.get('b',default=1)
    unit = request.GET.get('u',default=1)
    servicing_mfo = request.GET.get('s',default=1)

    data = {
        'budget':[budget],
        'unit':[unit],
        'servicing_mfo':[servicing_mfo]
    }
    user = request.user
    account = user.account
    filters = {}

    if data.get('budget'):
        releases = FundReleaseRecipient.objects.filter(
            fund_release_item__fund_release__budget_id__in=data['budget']).order_by('servicing_mfo', 'unit')
        filters['Budget Fund Source'] = ', '.join(Pawaf.objects.filter(pk__in=data['budget']).
                                                  values_list('description', flat=True))
    elif data.get('other_budget'):
        releases = FundReleaseRecipient.objects.filter(
            fund_release_item__fund_release__other_budget__iexact=data['other_budget']).order_by('servicing_mfo', 'unit')
        filters['Other Source'] = data['other_budget']
    else:
        return Response(status=status.HTTP_404_NOT_FOUND, headers={'Content-Type': 'application/json'})

    if data.get('servicing_mfo'):
        releases = releases.filter(servicing_mfo_id__in=data['servicing_mfo'])
        filters['Servicing MFO'] = ', '.join(Pamu.objects.filter(pk__in=data['servicing_mfo']).
                                             values_list('name', flat=True))

    if data.get('unit'):
        releases = releases.filter(unit_id__in=data['unit'])
        filters['Unit'] = ', '.join(Unit.objects.filter(pk__in=data['unit']).
                                    values_list('name', flat=True))

    if not account.special_permissions or 'can_rrf_cmd' not in account.special_permissions.get('ppb', []):
        releases = releases.filter(fund_release_item__fund_release__cmd=False)

    response = HttpResponse(content_type='application/ms-excel')

    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet('Sheet 1')
    releases = releases.\
        annotate(rrf_no=F('fund_release_item__fund_release__rrf_no'),
                 specific_purpose=F('fund_release_item__specific_purpose'),
                 status=F('fund_release_item__fund_release__status__name')).\
        order_by('rrf_no', 'servicing_mfo', 'unit', ).distinct()
    compose_summary_of_release(releases, sheet, filters)

    title = 'Summary of Releases'
    response['filename'] = f'{title}.xls'
    response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
    response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'
    wb.save(response)

    return response


@api_view(['GET'])
@permission_classes([])
def download_fund_utilization_summary(request, pk):
    data = request.data
    user = request.user
    account = user.account.account_dict()

    error_response = Response(status=status.HTTP_404_NOT_FOUND, headers={'Content-Type': 'application/json'})
    budget_item = None

    try:
        budget_record = Pawaf.objects.get(pk=pk)
    except Pawaf.DoesNotExist:
        return error_response

    budget_items = budget_record.pawaf_items.all()

    branch = account['organization'].upper()
    if branch != common_consts.PPB.upper():
        budget_items = budget_items.filter(branch__iexact=branch)
    else:
        branch = None

    if data.get('budget_item'):
        try:
            budget_item = budget_items.get(pk=data['budget_item'])
        except PawafItem.DoesNotExist:
            return error_response

    response = HttpResponse(content_type='application/ms-excel')

    wb = xlwt.Workbook(encoding='utf-8')
    compose_fund_monitoring(wb, budget_record, budget_item, branch)
    title = f'{budget_record.description} Fund Utilization'
    response['filename'] = f'{title}.xls'
    response['Content-Disposition'] = f'attachment; filename="{response["filename"]}"'
    response['Access-Control-Expose-Headers'] = 'filename, Content-Disposition'
    wb.save(response)

    return response


from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def write_pdf_rrf_view(request, pk):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, '.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def write_pdf_asa_view(request, pk):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, '.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response