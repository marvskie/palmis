from commons.permissions import BaseAuthenticatedPermission
from commons import consts


class EngineeringPermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if view.action in ['create', 'update', 'partial_update']:
            return account['organization'] == consts.EB
        elif view.action == 'destroy':
            return False
        elif view.action in ['list', 'retrieve']:
            return consts.is_og4(account['organization']) or account['organization'] == consts.PAMU
        return False


class RemarksPermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if view.action in ['create', 'update', 'partial_update']:
            return account['organization'] in [consts.EB, consts.PAMU]
        elif view.action in ['list', 'retrieve']:
            return consts.is_og4(account['organization']) or account['organization'] == consts.PAMU
        elif view.action == 'destroy':
            return account['organization'] == consts.EB
        return False


class ReportsPermission(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if request.method == 'POST':
            return consts.is_og4(account['organization']) or account['organization'] == consts.PAMU
        return False
