from commons.permissions import BaseAuthenticatedPermission
from commons import consts


class InstructionPermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return account['organization'] == consts.EXECUTIVE
        elif view.action in ['list', 'retrieve']:
            return consts.is_og4(account['organization'])

        return False
