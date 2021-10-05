from django.conf.urls import url, include
from rest_framework import routers

from mobility import views


router = routers.DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('tonnage', views.TonnageViewSet)
router.register('type', views.TypeViewSet)
router.register('nomenclature', views.NomenclatureViewSet)
router.register('vehicle_record', views.VehicleRecordViewSet)
router.register('repair_record', views.RepairRecordViewSet)
router.register('tire/fssu', views.TireRecordViewSet)
router.register('battery/fssu', views.BatteryRecordViewSet)
router.register('tire_nomenclature', views.NomenclatureTireViewSet)
router.register('battery_nomenclature', views.NomenclatureBatteryViewSet)
router.register('vehicle_remarks', views.VehicleRemarksViewSet)

urlpatterns = [
    url(r'^mobility/', include(router.urls)),
    url(r'^mobility/transport_type/$', views.get_transport_type),
    url(r'^mobility/repair_implementation/$', views.get_repair_implementation),
    url(r'^mobility/report/repair_status/$', views.export_repair)
]
