from django.conf.urls import url, include
from rest_framework import routers

from camb import views

router = routers.DefaultRouter()

# --- NEW PALMIS urls 
router.register('das_projects', views.DASProjectsViewSet)
router.register('fms_projects', views.FMSProjectsViewSet)
router.register('srdp_projects', views.SRDPProjectsViewSet)
router.register('int_log_activities', views.InternationLogisticsActivitiesViewSet)
router.register('draft_documents', views.DraftDocumentsViewSet)
router.register('ref_help_links', views.ReferencesHelpfulLinksViewSet)
router.register('ref_defense_exhibits', views.ReferencesDefenseExhibitsViewSet)
router.register('ref_policies', views.ReferencesPoliciesViewSet)
router.register('ref_brochures', views.ReferencesBrochuresViewSet)
router.register('incommint_commo', views.IncomingCommunicationViewSet)
router.register('outgoing_commo', views.OutgoingCommunicationViewSet)


urlpatterns = [
    url(r'^camb/', include(router.urls)),
]
