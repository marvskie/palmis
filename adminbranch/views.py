import logging
from datetime import datetime

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions as api_permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from adminbranch import models
from adminbranch import serializers

logger = logging.getLogger(__name__)

# ======== NEW PALMIS views
class RosterOfTroopsViewSet(viewsets.ModelViewSet):
    queryset = models.RosterOfTroops.objects.all()
    serializer_class = serializers.RosterOfTroopsSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class AdminMooeViewSet(viewsets.ModelViewSet):
    queryset = models.AdminMooe.objects.all()
    serializer_class = serializers.AdminMooeSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class AdminEquipmentViewSet(viewsets.ModelViewSet):
    queryset = models.AdminEquipment.objects.all()
    serializer_class = serializers.AdminEquipmentSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class IncomingCommunicationViewSet(viewsets.ModelViewSet):
    queryset = models.IncomingCommunication.objects.all()
    serializer_class = serializers.IncomingCommunicationSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class OutgoingCommunicationViewSet(viewsets.ModelViewSet):
    queryset = models.OutgoingCommunication.objects.all()
    serializer_class = serializers.OutgoingCommunicationSerializer
    permission_classes = [api_permissions.IsAuthenticated]
