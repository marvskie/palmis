import random
import string
from django.utils import timezone
from django_otp.oath import TOTP
from preferences.models import SystemPreference
from rest_sms_gateway import SMSGatewayClient


LOGIN = 'login'
CHANGE_PASSWORD = 'change_password'
FORGOT_PASSWORD = 'forgot_password'


class FMISOTP:
    ACTIONS = {
        LOGIN: 'log-in your FMIS account',
        CHANGE_PASSWORD: 'change your password',
        FORGOT_PASSWORD: 'to recover your FMIS account'
    }

    def __init__(self, user, action=LOGIN):
        self.otp_validity = int(SystemPreference.objects.get_value('otp_validity'))
        self.otp_host = SystemPreference.objects.get_value('otp_host')
        self.otp_msg = SystemPreference.objects.get_value('otp_sms_msg')
        self.username = user.username if user else ''
        self.mobile_number = user.account.mobile_no
        self.action = self.ACTIONS.get(action, '')

    def get_otp(self):
        ref_num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        totp_key = f'{self.username}{ref_num}'
        totp = TOTP(key=bytearray(totp_key, 'utf-8'), step=self.otp_validity)
        return ref_num, totp.token()

    def send_otp_sms(self, ref_num, otp_token):
        now = timezone.localtime(timezone.now())
        date_formatted = now.strftime('%d-%b %Y %I:%M%p')
        client = SMSGatewayClient(self.otp_host)
        _ = client.send_sms(self.mobile_number, self.otp_msg.format(token=otp_token, action=self.action, time=date_formatted, ref_number=ref_num))

    def verify_otp(self, ref_num, otp_token):
        totp_key = f'{self.username}{ref_num}'
        totp = TOTP(key=bytearray(totp_key, 'utf-8'), step=self.otp_validity)
        return totp.verify(int(otp_token))
