from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib import admin
from famis import views
admin.autodiscover()
urlpatterns = [
    path('', admin.site.urls),
    url(r'^chat/', include('core_chat.urls')),
    url(r'^custom/', include('custom_pages.urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/v1/', include('narra.urls_api_v1')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

