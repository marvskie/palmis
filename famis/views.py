import logging
from datetime import datetime

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions as api_permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from famis import models
from famis import serializers

logger = logging.getLogger(__name__)

# ======== NEW PALMIS views

# class FacilityViewSet(viewsets.ModelViewSet):
#     queryset = models.Facility.objects.all()
#     serializer_class = serializers.FacilitySerializer
#     permission_classes = [api_permissions.IsAuthenticated]

class FacilityInfoViewSet(viewsets.ModelViewSet):
    queryset = models.FacilityInfo.objects.all()
    serializer_class = serializers.FacilityInfoSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class FacilityMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = models.FacilityMaintenance.objects.all()
    serializer_class = serializers.FacilityMaintenanceSerializer
    permission_classes = [api_permissions.IsAuthenticated]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = models.Inventory.objects.all()
    serializer_class = serializers.InventorySerializer
    permission_classes = [api_permissions.IsAuthenticated]





