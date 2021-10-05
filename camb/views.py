import logging
from datetime import datetime

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions as api_permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from camb import models
from camb import serializers

logger = logging.getLogger(__name__)

# ======== NEW PALMIS views

class DASProjectsViewSet(viewsets.ModelViewSet):
    queryset = models.DASProjects.objects.all()
    serializer_class = serializers.DASProjectsSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class FMSProjectsViewSet(viewsets.ModelViewSet):
    queryset = models.FMSProjects.objects.all()
    serializer_class = serializers.FMSProjectsSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class SRDPProjectsViewSet(viewsets.ModelViewSet):
    queryset = models.SRDPProjects.objects.all()
    serializer_class = serializers.SRDPProjectsSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class InternationLogisticsActivitiesViewSet(viewsets.ModelViewSet):
    queryset = models.InternationalLogisticsActivities.objects.all()
    serializer_class = serializers.InternationalLogisticsActivitiesSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class DraftDocumentsViewSet(viewsets.ModelViewSet):
    queryset = models.DraftDocuments.objects.all()
    serializer_class = serializers.DraftDocumentsSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ReferencesHelpfulLinksViewSet(viewsets.ModelViewSet):
    queryset = models.ReferencesHelpfulLinks.objects.all()
    serializer_class = serializers.ReferencesHelpfulLinksSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ReferencesDefenseExhibitsViewSet(viewsets.ModelViewSet):
    queryset = models.ReferencesDefenseExhibits.objects.all()
    serializer_class = serializers.ReferencesDefenseExhibitsSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ReferencesPoliciesViewSet(viewsets.ModelViewSet):
    queryset = models.ReferencesPolicies.objects.all()
    serializer_class = serializers.ReferencesPoliciesSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class ReferencesBrochuresViewSet(viewsets.ModelViewSet):
    queryset = models.ReferencesBrochures.objects.all()
    serializer_class = serializers.ReferencesBrochuresSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class IncomingCommunicationViewSet(viewsets.ModelViewSet):
    queryset = models.IncomingCommunication.objects.all()
    serializer_class = serializers.IncomingCommunicationSerializer
    permission_classes = [api_permissions.IsAuthenticated]

class OutgoingCommunicationViewSet(viewsets.ModelViewSet):
    queryset = models.OutgoingCommunication.objects.all()
    serializer_class = serializers.OutgoingCommunicationSerializer
    permission_classes = [api_permissions.IsAuthenticated]
