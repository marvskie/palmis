from django.conf.urls import url, include
from rest_framework import routers

from camb import views

router = routers.DefaultRouter()

# --- NEW PALMIS urls 
# router.register('das_projects', views.DASProjectsViewSet)



urlpatterns = [
    url(r'^lob/', include(router.urls)),
]
