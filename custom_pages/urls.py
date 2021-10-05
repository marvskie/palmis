from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

# from core_chat.api import MessageModelViewSet, UserModelViewSet

router = DefaultRouter()
# router.register(r'message', MessageModelViewSet, basename='message-api')
# router.register(r'user', UserModelViewSet, basename='user-api')

urlpatterns = [
    url(r'^calendar/', login_required(
        TemplateView.as_view(template_name='custom_pages/calendar.html')), name='calendar'),
]
