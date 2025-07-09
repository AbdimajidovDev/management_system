from django.urls import path
from app.reports.views import teacher_salary_view


urlpatterns = [
    path('teacher-salary/',teacher_salary_view, name='teacher_salary' ),
    # path('payment/<int:uuid>', ),
]
