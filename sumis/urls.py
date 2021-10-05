from django.conf.urls import url, include
from django.views.generic import RedirectView

urlpatterns += [
    path('sumis/', include('sumis.urls')),
    path('', RedirectView.as_view(url='sumis/', permanent=True)),
]