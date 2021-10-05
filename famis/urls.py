from django.conf.urls import url, include
from rest_framework import routers

from famis import views

router = routers.DefaultRouter()

# --- NEW PALMIS urls 
router.register('', views.InventoryViewSet)
# router.register('', views.FacilityViewSet)
router.register('', views.FacilityInfoViewSet)
router.register('', views.FacilityMaintenanceViewSet)

urlpatterns = [
    url(r'^famis/', include(router.urls)),
]