from django.template.response import TemplateResponse
from app.groups.models import Group
from app.students.models import StudentGroup


def dashboard_view(request):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    current_year = now().year
    added_data = []
    removed_data = []
    active_data = []

    for month in range(1, 13):
        #  shu oyda Qo‘shilgan studentlar
        added = Student.objects.filter(
            created_at__year=current_year,
            created_at__month=month
        ).count()

        # Ketganlar
        removed = Student.objects.filter(
            is_active=False,
            updated_at__year=current_year,
            updated_at__month=month
        ).count()

        # Shu oy oxirida mavjud aktivlar
        active = Student.objects.filter(
            is_active=True,
            created_at__year__lte=current_year,
            created_at__month__lte=month
        ).count()

        added_data.append(added)
        removed_data.append(removed)
        active_data.append(active)

    labels = [g.name for g in Group.objects.all()]
    data = [Student.objects.filter(groups=g).count() for g in Group.objects.all()]

    context = {
        'labels': labels,
        'data': data,

        "months": months,
        "added": added_data,
        "removed": removed_data,
        "active": active_data,
    }

    return TemplateResponse(request, "unfold/dashboard.html", context)

# ----------------------------------------------------------------------------->

from django.utils.timezone import now
from calendar import monthrange
from app.students.models import Student
from app.attendance.models import Attendance

def attendance_chart_view(request):
    selected_month = int(request.GET.get('month', now().month))
    selected_year = int(request.GET.get('year', now().year))

    days_in_month = monthrange(selected_year, selected_month)[1]
    labels = [str(day) for day in range(1, days_in_month + 1)]

    total_counts = []
    present_counts = []

    for day in range(1, days_in_month + 1):
        day_present = Attendance.objects.filter(
            date__year=selected_year,
            date__month=selected_month,
            date__day=day,
            status='p'
        ).count()

        # Shu kunga qadar qo‘shilgan active studentlar soni
        day_total = StudentGroup.objects.filter(
            created_at__lte=f"{selected_year}-{selected_month:02d}-{day:02d}"
        ).count()

        present_counts.append(day_present)
        total_counts.append(day_total)

    months = [
        {"value": i, "label":month_name}
        for i, month_name in enumerate(
            ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun", "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"], 1
        )
    ]

    context = {
        'labels': labels,
        'total_counts': total_counts,
        'present_counts': present_counts,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': months,
    }

    return TemplateResponse(request, "admin/attendance_chart.html", context)
