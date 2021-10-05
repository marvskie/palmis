from django.conf.urls import url, include
from rest_framework import routers

from message import views


router = routers.DefaultRouter()
router.register('remarks', views.MessageViewSet)

urlpatterns = [
    url(r'^message/', include(router.urls)),
]
