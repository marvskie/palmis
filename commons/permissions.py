from rest_framework import permissions
from rest_condition import And, Or

from commons import consts


AND = And
OR = Or


def user_account(user):
    # has account
    # account.active = True
    # has active_role
    # has active division

    if not user or not hasattr(user, 'account'):
        return None

    account_dict = user.account.account_dict()

    if not account_dict['active'] or not account_dict['role'] or \
            (not consts.is_hpa(account_dict['organization']) and not account_dict['division']):
        return None

    return account_dict


class BaseAuthenticatedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_authenticated = user and user.is_authenticated
        if not is_authenticated:
            return False

        account = user_account(user)

        if not account:
            return False

        return self.has_access(request, view, account)

    def has_access(self, request, view, account, **kwargs):
        return True


class IsEB(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        return account['organization'] == consts.EB


class IsAB(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        return account['organization'] == consts.ADMIN


class IsOG4(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        return consts.is_og4(account['organization'])


class IsPPB(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        return account['organization'] == consts.PPB


class IsExecutive(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        return account['organization'] == consts.EXECUTIVE


class IsExecutiveReadable(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        return account['organization'] == consts.EXECUTIVE and view.action in ['list', 'retrieve']


class IsOG4Readable(BaseAuthenticatedPermission):
    def has_access(self, request, view, account, **kwargs):
        if view.action in ['list', 'retrieve']:
            return consts.is_og4(account['organization'])
        return False
