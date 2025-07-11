from datetime import datetime

from django.shortcuts import render
from drf_spectacular.utils import extend_schema

from app.groups.models import Group
from app.reports.utility import calculate_teacher_salary


@extend_schema(tags=['teacher'])
def teacher_salary_view(request):
    teacher = request.user
    groups = Group.objects.filter(teacher=teacher)

    group_id = request.GET.get('group')
    group = groups.filter(id=group_id).first() if group_id else groups.first()

    month = int(request.GET.get('month', datetime.now().month))
    year = int(request.GET.get('year', datetime.now().year))

    salary = None
    if group:
        salary = calculate_teacher_salary(group, month, year)
    return render(request, 'salaries/teacher_salary.html',{
        'groups': groups,
        'group': group,
        'month': month,
        'year': year,
        'salary': salary})
