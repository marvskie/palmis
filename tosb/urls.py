from django.conf.urls import url, include
from rest_framework import routers

from tosb import views


router = routers.DefaultRouter()
router.register('icie_nomenclature', views.NomenclatureIcieViewSet)
router.register('icie/fssu', views.IcieRecordViewSet)

urlpatterns = [
    url(r'^tosb/', include(router.urls))
]
