from commons.permissions import BaseAuthenticatedPermission
from commons import consts


class PawafPermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return account['role'] == consts.PPB_CHIEF

        return consts.is_og4(account['organization'])
