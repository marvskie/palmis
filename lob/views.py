import logging
from datetime import datetime

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions as api_permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from lob import models
from lob import serializers

logger = logging.getLogger(__name__)

# ======== NEW PALMIS views

