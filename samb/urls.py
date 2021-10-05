from django.conf.urls import url, include
from rest_framework import routers

from samb import views

router = routers.DefaultRouter()

# --- NEW PALMIS urls 
# router.register('das_projects', views.RosterOfTroopsViewSet)
# router.register('das_projects', views.AdminMooeViewSet)
# router.register('das_projects', views.AdminEquipmentViewSet)
# router.register('das_projects', views.IncomingCommunicationViewSet)
# router.register('das_projects', views.OutgoingCommunicationViewSet)

urlpatterns = [
    url(r'^samb/', include(router.urls)),
]
