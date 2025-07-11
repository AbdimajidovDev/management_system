from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.attendance'

    # def ready(self):
    #     import app.attendance.signals
