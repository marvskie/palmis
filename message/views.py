import logging

from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response

from commons import consts as commons_consts
from message import serializers
from message import models
from message import filters


logger = logging.getLogger(__name__)


class MessageViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    model = models.Message
    filter_class = filters.MessageFilter
    queryset = models.Message.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.MessageSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return serializers.MessageCUSerializer

    def get_content_type(self):
        # Return content type id
        return None

    def get_object_id(self):
        return 0

    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = request.data

        data['content_type'] = self.get_content_type()
        data['object_id'] = self.get_object_id()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=user, updated_by=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        user = self.request.user
        data = request.data

        if user != instance.created_by:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        m_data = {'remarks': data.get('remarks')}

        serializer = self.get_serializer(instance, data=m_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=user)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if self.action == 'list' and not self.get_object_id():
            queryset = models.Message.objects.none()
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        account = user.account.account_dict()
        queryset = models.Message.objects.none()

        if commons_consts.is_og4(account['organization']):
            queryset = models.Message.objects.all()
        elif account['organization'] == commons_consts.PAMU:
            queryset = self.get_pamu_queryset()
        else:
            queryset = models.Message.objects.none()

        if self.get_object_id():
            queryset = queryset.filter(object_id=self.get_object_id())
        if self.get_content_type():
            queryset = queryset.filter(content_type_id=self.get_content_type())

        return queryset.order_by('-created_at')

    def get_pamu_queryset(self):
        return models.Message.objects.none()
