from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from commons import filters
from commons import serializers
from commons import models
from commons import consts
from commons import permissions


class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin):
    model = models.Account
    queryset = models.Account.objects.all().order_by('user__username')
    permission_classes = [permissions.IsAB]
    filter_class = filters.AccountFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.AccountSerializer
        # TODO create, update serializer


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Branch
    queryset = models.Branch.objects.all().order_by('order')


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Organization
    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class PamuViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Pamu
    queryset = models.Pamu.objects.all()
    serializer_class = serializers.PamuSerializer


class FssuViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Fssu
    queryset = models.Fssu.objects.all()
    serializer_class = serializers.FssuSerializer


class SprsViewSet(viewsets.ModelViewSet):
    model = models.Sprs
    queryset = models.Sprs.objects.all()
    serializer_class = serializers.SprsSerializer


class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Unit
    queryset = models.Unit.objects.none()
    serializer_class = serializers.UnitSerializer
    filter_class = filters.UnitFilter

    def get_queryset(self):
        user = self.request.user
        account = user.account.account_dict()

        if consts.is_og4(account['organization']):
            return models.Unit.objects.all()
        elif account['organization'] == consts.PAMU:
            return models.Unit.objects.filter(pamu=account['division'])
        return models.Unit.objects.none()


class ServiceabilityViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Serviceability
    queryset = models.Serviceability.objects.all()
    serializer_class = serializers.ServiceabilitySerializer


class AcquisitionModeViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.AcquisitionMode
    queryset = models.AcquisitionMode.objects.all()
    serializer_class = serializers.AcquisitionModeSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.Region
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionSerializer


class ProcurementModeViewSet(viewsets.ReadOnlyModelViewSet):
    model = models.ProcurementMode
    queryset = models.ProcurementMode.objects.all().order_by('order')
    serializer_class = serializers.ProcurementModeSerializer


@api_view(['GET'])
def get_geographical_location(request):
    data = [
        {'code': code, 'name': val} for code, val in models.MAJOR_ISLANDS
    ]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_quarter(request):
    data = [
        {'code': code, 'name': val} for code, val in models.QUARTER_CHOICES
    ]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])
def my_profile(request):
    print(request)
    user = request.user
    account = user.account

    profile = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'require_change_pw': account.require_change_pw,
        'profile': {
            'organization': {
                'code': account.role.organization.code,
                'name': account.role.organization.name,
                'id': account.role.organization.pk

            },
            'role': {
                'code': account.role.code,
                'name': account.role.name
            },
            'division': None,
            'is_cmd': account.is_cmd()
        }
    }

    division = account.division()

    if division:
        profile['profile']['division'] = {
            'code': division.code,
            'name': division.name
        }

    return Response(profile, status=status.HTTP_200_OK)
