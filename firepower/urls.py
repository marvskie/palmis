from django.conf.urls import url, include
from rest_framework import routers

from firepower import views

router = routers.DefaultRouter()

# --- NEW PALMIS urls 
router.register('ammunition_exp', views.ExpenditureAmmunitionViewSet)
router.register('programs_demil', views.ProgramsDemilitarizationViewSet)
router.register('programs_disposal', views.ProgramsDisposalViewSet)
router.register('programs_repair', views.ProgramsRepairAndMaintenanceViewSet)
router.register('programs_procurement', views.ProgramsProcurementViewSet)
router.register('toe_mother_unit', views.TOEMotherUnitViewSet)
router.register('toe_pa_wide', views.TOEPaWideViewSet)
router.register('status_of_fill_up', views.StatusOfFillUpViewSet)
router.register('spare_parts', views.SparePartsViewSet)
router.register('accessories', views.AccessoriesViewSet)
router.register('ammunition', views.AmmunitionViewSet)
router.register('firearm', views.FirearmViewSet)
router.register('incoming_commo', views.IncomingCommunicationViewSet)
router.register('outgoing_commo', views.OutgoingCommunicationViewSet)


urlpatterns = [
    url(r'^fpb/', include(router.urls)),
]
