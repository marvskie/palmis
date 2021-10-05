from django.conf.urls import url, include
from rest_framework import routers
from ppb import views

router = routers.DefaultRouter()
router.register('expense_class', views.ExpenseClassViewSet)
router.register('object_code', views.ObjectCodeViewSet)
router.register('mission_area', views.MissionAreaViewSet)
router.register('dpg', views.DpgViewSet)
router.register('strategic_objective', views.StrategicObjectiveViewSet)
router.register('strategic_program', views.StrategicProgramViewSet)
router.register('pbdg_objective', views.PbdgObjectiveViewSet)
router.register('program_objective', views.ProgramObjectiveViewSet)
router.register('kma', views.KmaViewSet)
router.register('major_pap', views.MajorPapViewSet)
router.register('sub_pap', views.SubPapViewSet)
router.register('suggested_pap', views.SuggestedPapViewSet)
router.register('pawaf', views.PawafViewSet)
router.register('pawaf_item', views.PawafItemViewSet)
router.register('view_by', views.PawafItemViewViewSet)
router.register('pawaf_item_end_user', views.PawafItemEndUserViewSet)
router.register('fund_release', views.FundReleaseViewSet)
router.register('fund_release_item', views.FundReleaseItemViewSet)
router.register('budget_breakdown_choices', views.PawaItemBudgetBreakdownForRrfSelectionViewSet)
router.register('status', views.StatusViewSet)
router.register('fund_release_asa', views.FundReleaseAsaViewSet)
router.register('key_program', views.KeyProgramViewSet)

urlpatterns = [
    url(r'ppb/', include(router.urls)),
    url(r'^ppb/pawaf/(?P<pk>[0-9]+)/download/$', views.download_budget_summary),
    url(r'^ppb/fund_release/(?P<pk>[0-9]+)/download/$', views.download_rrf),
    url(r'^ppb/pawaf/(?P<pk>[0-9]+)/download_utilization/$', views.download_fund_utilization_summary),
    url(r'^ppb/program/$', views.get_programs),
    url(r'^ppb/apb/(?P<pk>[0-9]+)/download/$', views.download_apb_monitor),
    url(r'^ppb/report/rrf_summary/$', views.download_summary_of_release),
]
