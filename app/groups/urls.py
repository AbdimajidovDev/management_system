from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.groups.views import GroupViewSet


router = DefaultRouter()
router.register('groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
