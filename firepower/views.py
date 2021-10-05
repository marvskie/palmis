import logging
from datetime import datetime

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions as api_permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from firepower import models
from firepower import serializers
from firepower import filters
from firepower import permissions

logger = logging.getLogger(__name__)

# ======== NEW PALMIS views

class ExpenditureAmmunitionViewSet(viewsets.ModelViewSet):
    queryset = models.ExpenditureAmmunition.objects.all()
    serializer_class = serializers.ExpenditureAmmunitionSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ProgramsDemilitarizationViewSet(viewsets.ModelViewSet):
    queryset = models.ProgramsDemilitarization.objects.all()
    serializer_class = serializers.ProgramsDemilitarizationSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ProgramsDisposalViewSet(viewsets.ModelViewSet):
    queryset = models.ProgramsDisposal.objects.all()
    serializer_class = serializers.ProgramsDisposalSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ProgramsRepairAndMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = models.ProgramsRepairAndMaintenance.objects.all()
    serializer_class = serializers.ProgramsRepairAndMaintenanceSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ProgramsProcurementViewSet(viewsets.ModelViewSet):
    queryset = models.ProgramsProcurement.objects.all()
    serializer_class = serializers.ProgramsProcurementSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class TOEMotherUnitViewSet(viewsets.ModelViewSet):
    queryset = models.TOEMotherUnit.objects.all()
    serializer_class = serializers.TOEMotherUnitSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class TOEPaWideViewSet(viewsets.ModelViewSet):
    queryset = models.TOEPaWide.objects.all()
    serializer_class = serializers.TOEPaWideSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class StatusOfFillUpViewSet(viewsets.ModelViewSet):
    queryset = models.StatusOfFillUp.objects.all()
    serializer_class = serializers.StatusOfFillUpSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class SparePartsViewSet(viewsets.ModelViewSet):
    queryset = models.SpareParts.objects.all()
    serializer_class = serializers.SparePartsSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class AccessoriesViewSet(viewsets.ModelViewSet):
    queryset = models.Accessories.objects.all()
    serializer_class = serializers.AccessoriesSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class AmmunitionViewSet(viewsets.ModelViewSet):
    queryset = models.Ammunition.objects.all()
    serializer_class = serializers.AmmunitionSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class FirearmViewSet(viewsets.ModelViewSet):
    queryset = models.Firearm.objects.all()
    serializer_class = serializers.FirearmSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class IncomingCommunicationViewSet(viewsets.ModelViewSet):
    queryset = models.IncomingCommunication.objects.all()
    serializer_class = serializers.IncomingCommunicationSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class OutgoingCommunicationViewSet(viewsets.ModelViewSet):
    queryset = models.OutgoingCommunication.objects.all()
    serializer_class = serializers.OutgoingCommunicationSerializer
    permission_classes = [api_permissions.IsAuthenticated]