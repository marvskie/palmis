from django.conf.urls import url, include
from rest_framework import routers

from commons import views


router = routers.DefaultRouter()
router.register('account', views.AccountViewSet)
router.register('organization', views.OrganizationViewSet)
router.register('pamu', views.PamuViewSet)
router.register('fssu', views.FssuViewSet)
router.register('unit', views.UnitViewSet)
router.register('serviceability', views.ServiceabilityViewSet)
router.register('acquisition_mode', views.AcquisitionModeViewSet)
router.register('region', views.RegionViewSet)
router.register('procurement_mode', views.ProcurementModeViewSet)
router.register('sprs', views.SprsViewSet)


urlpatterns = [
    url(r'^commons/', include(router.urls)),
    url(r'^my_profile/$', views.my_profile),
    url(r'^commons/geographical_location/$', views.get_geographical_location),
    url(r'^commons/quarter/$', views.get_quarter)
]
