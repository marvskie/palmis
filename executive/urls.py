from django.conf.urls import include, url
from rest_framework import routers

from executive import views

router = routers.DefaultRouter()
router.register('instruction', views.InstructionRecordViewSet)

urlpatterns = [
    url(r'^executive/', include(router.urls)),
]
