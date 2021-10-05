from django.conf.urls import url, include
urlpatterns = [
    url(r'', include('commons.urls')),
    url(r'', include('login.urls')),
    url(r'', include('ppb.urls')),
    url(r'', include('mobility.urls')),
    url(r'', include('engineering.urls')),
    url(r'', include('tosb.urls')),
    url(r'', include('message.urls')),
    url(r'', include('executive.urls')),
    url(r'', include('exec.urls')),
]
