import logging

from rest_framework import viewsets

from commons import consts as commons_consts
from executive import models, serializers, permissions

logger = logging.getLogger(__name__)


class InstructionRecordViewSet(viewsets.ModelViewSet):
    model = models.InstructionRecord
    queryset = models.InstructionRecord.objects.none()
    serializer_class = serializers.InstructionRecordSerializer
    permission_classes = [permissions.InstructionPermission]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)

    def get_queryset(self):
        user = self.request.user
        account = user.account.account_dict()

        if account['organization'] == commons_consts.EXECUTIVE:
            return models.InstructionRecord.objects.all()
        elif commons_consts.is_og4(account['organization']):
            return models.InstructionRecord.objects.filter(recipients__branch__code=account['organization'])
        return self.queryset
