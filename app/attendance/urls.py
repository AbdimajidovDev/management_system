from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.attendance.views import *

router = DefaultRouter()
router.register('attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("save/", save_attendance, name="save_attendance"),
]
