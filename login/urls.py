from django.conf.urls import url
from login.views import login, refresh_token, logout, change_password, verify_login_otp


urlpatterns = [
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^token/$', refresh_token),
    url(r'^otp/$', verify_login_otp),
    url(r'password/change/$', change_password)
]
