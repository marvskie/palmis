import random
import string
import hashlib
import logging

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from oauth2_provider.models import AccessToken, Application, RefreshToken

from preferences.models import SystemPreference
from login.otp import FMISOTP
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def generate_token(user):
    seq = string.digits + string.ascii_letters
    salt = ''.join(random.choices(seq, k=16))
    token = f'{user.username}.{user.date_joined.strftime("%Y-%m-%d %H:%M:%S")}.{salt}'
    return hashlib.md5(token.encode('utf-8')).hexdigest()


def create_token_obj(user, app):
    expire_seconds = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
    scopes = settings.OAUTH2_PROVIDER['SCOPES']
    expires = timezone.localtime() + timezone.timedelta(seconds=expire_seconds)

    # Delete old tokens of this user, if any
    RefreshToken.objects.filter(user=user, application=app).delete()
    AccessToken.objects.filter(user=user, application=app).delete()

    access_token = AccessToken.objects.create(
        user=user,
        application=app,
        token=generate_token(user),
        expires=expires,
        scope=scopes)

    refresh_token_ = RefreshToken.objects.create(
        user=user,
        application=app,
        token=generate_token(user),
        access_token=access_token)

    return {
        'access_token': access_token.token,
        'token_type': 'Bearer',
        'expires_in': expire_seconds - 3,  # assume 3 seconds delivery delay
        'refresh_token': refresh_token_.token,
    }


@api_view(['POST'])
@permission_classes([])
@csrf_exempt
def login(request):
    data = request.POST or request.data
    username = data.get('username', '')
    passwd = data.get('password', '')
    application = data.get('application', '')
    print(data)
    user = authenticate(username=username, password=passwd)
    print(user)
    if not user or not user.account or not user.account.active:
        return Response(data={'data': 'Incorrect username/password.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        app = Application.objects.get(name=application)
    except Application.DoesNotExist:
        return Response(data={'data': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

    # check if OTP is required
    require_otp = SystemPreference.objects.get_value('require_otp')
    bypass_otp = user.account.bypass_otp

    print('creating tokens....')
    if not require_otp or bypass_otp:
        tokens = create_token_obj(user, app)
    else:
        fmisotp = FMISOTP(user)
        ref_num, otp_token = fmisotp.get_otp()
        fmisotp.send_otp_sms(ref_num, otp_token)
        tokens = {'data': 'OK', 'ref_num': ref_num}
    print(tokens)
    return Response(data=tokens, status=status.HTTP_200_OK)


@csrf_exempt
def verify_login_otp(request):
    data = request.POST or request.data
    username = data.get('username', '')
    passwd = data.get('password', '')
    application = data.get('application', 'kamagong')
    ref_number = data.get('ref_number', '')
    otp_token = data.get('otp', '')

    user = authenticate(username=username, password=passwd)
    fmisotp = FMISOTP(user)

    if user and fmisotp.verify_otp(ref_number, otp_token):
        try:
            app = Application.objects.get(name=application)
        except Application.DoesNotExist:
            return JsonResponse(data={'data': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
        tokens = create_token_obj(user, app)
        resp_status = status.HTTP_200_OK
    else:
        tokens = {'data': 'NOT OK'}
        resp_status = status.HTTP_400_BAD_REQUEST

    return JsonResponse(tokens, status=resp_status)


@api_view(['POST'])
@permission_classes([])
@csrf_exempt
def refresh_token(request):
    data = request.POST or request.data
    token = data.get('refresh_token', '')
    application = data.get('application', '')

    try:
        app = Application.objects.get(name=application)
        refresh_token_obj = RefreshToken.objects.get(token=token, application=app)
    except RefreshToken.DoesNotExist:
        return Response(data={'data': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    user = refresh_token_obj.user

    if not user.account and not user.account.active:
        return Response(data={'data': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

    tokens = create_token_obj(user, app)

    return Response(data=tokens, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def logout(request):
    
    user = request.user
    print(user)
    data = request.POST or request.data
    application = data.get('application', '')

    app = Application.objects.get(name=application)

    RefreshToken.objects.filter(user=user, application=app).delete()
    AccessToken.objects.filter(user=user, application=app).delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def change_password(request):
    user = request.user
    data = request.POST or request.data

    account = user.account
    if not account:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')

    verified_user = authenticate(username=user.username, password=current_password)
    if not verified_user:
        return Response(data={'data': 'Incorrect current password.'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password == current_password:
        return Response(data={'data': 'Cannot use the old password.'}, status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response(data={'data': 'Passwords did not match.'}, status=status.HTTP_400_BAD_REQUEST)

    # OTP not required or OTP verified
    user.set_password(new_password)
    user.save()

    account.require_change_pw = False
    account.save()

    return Response(data={'data': 'Password successfully changed.'}, status=status.HTTP_200_OK)
