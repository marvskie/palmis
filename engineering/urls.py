from django.conf.urls import url, include
from rest_framework import routers

from engineering import views

router = routers.DefaultRouter()
# router.register('co_status', views.CoStatusViewSet)
# router.register('co_project_record', views.CoProjectRecordViewSet)
# router.register('reservation_record', views.ReservationRecordViewSet)
# router.register('building_record', views.BuildingRecordViewSet)
# router.register('repair_record', views.RepairRecordViewSet)
# router.register('building_category', views.BuildingCategoryViewSet)
# router.register('co_project_remarks', views.CoProjectRemarksViewSet)
# router.register('building_remarks', views.BuildingRemarksViewSet)
# router.register('reservation_remarks', views.ReservationRemarksViewSet)

# --- NEW PALMIS urls 
router.register('heavy_equipment', views.HeavyEquipmentViewSet)
router.register('light_equipment', views.LightEquipmentViewSet)
router.register('light_record', views.LightRecordViewSet)
router.register('water_record', views.WaterRecordViewSet)
router.register('insurance_of_building', views.InsuranceOfBuildingViewSet)
router.register('survey_titling_fencing', views.SurveyTitlingFencingViewSet)
router.register('lot_rental', views.LotRentalViewSet)
router.register('detailed_arch', views.DetailedArchitecturalAndEngineeringDesignViewSet)
router.register('cmdp', views.ComprehensiveMasterDevelopmentPlanViewSet)
router.register('capital_outlay', views.CapitalOutlayViewSet)
router.register('interagency_transfer_fund', views.InteragencyTransferFundViewSet)
router.register('bcda', views.BasesConversionAndDevelopmentAuthorityViewSet)
router.register('incoming_commo', views.IncomingCommunicationViewSet)
router.register('outgoing_commo', views.OutgoingCommunicationViewSet)


urlpatterns = [
    url(r'^eb/', include(router.urls)),
    # url(r'^eb/report/repair_status/$', views.export_repair),
    # url(r'^eb/report/co_status/$', views.export_co),
    # url(r'^eb/report/co_list/$', views.export_co_list),
    # url(r'^eb/report/building_record_list/$', views.export_facility_list),
    # url(r'^eb/report/reservation_list/$', views.export_reservation_list),
]
