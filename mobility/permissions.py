from commons.permissions import BaseAuthenticatedPermission
from commons import consts


class VehiclePermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if view.action == 'create':
            return account['organization'] == consts.MB
        elif view.action in ['update', 'partial_update']:
            return account['organization'] == consts.MB or account['organization'] == consts.PAMU
        elif view.action == 'destroy':
            return False

        return consts.is_og4(account['organization']) or consts.PAMU


class VehicleRepairPermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if view.action in ['update', 'partial_update', 'create']:
            return account['organization'] == consts.MB
        return consts.is_og4(account['organization']) or consts.PAMU


class RemarksPermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if view.action in ['create', 'update', 'partial_update']:
            return account['organization'] in [consts.MB, consts.PAMU]
        elif view.action in ['list', 'retrieve']:
            return consts.is_og4(account['organization']) or account['organization'] == consts.PAMU
        return False


class ReportsPermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if request.method == 'POST':
            return consts.is_og4(account['organization']) or account['organization'] == consts.PAMU
        return False

