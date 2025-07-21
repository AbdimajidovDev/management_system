from datetime import datetime
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from app.users.models import User
from app.users.permissions import IsTeacher, IsAdminOrSuperAdmin
from app.students.models import Student
from app.groups.models import Group

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrSuperAdmin | IsTeacher]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == User.UserRoles.teacher:
            return Attendance.objects.filter(group__teacher=user)
        elif user.role == User.UserRoles.superadmin or User.UserRoles.admin:
            return Attendance.objects.all()
        return Attendance.objects.none()

    def perform_create(self, serializer):
        student = serializer.validated_data["student"]
        user = self.request.user
        group = serializer.validated_data.get('group')

        if user.role == User.UserRoles.teacher:
            if group.teacher != user:
                data = {
                    'success': False,
                    'message': "Siz faqat o'z guruhlaringizga yo'qlama kirita olasiz!"
                }
                raise PermissionDenied(data)
        if not student in group.students.all():
            data = {
                'success': False,
                'message': "Siz faqat o'zingizga tegishli gurux talabalarini yo'qlama qila olasiz!"
            }
            raise PermissionDenied(data)
        serializer.save()


@csrf_exempt
def save_attendance(request):

    if request.method == "POST":
        group_id = request.POST.get("group_id")
        group = Group.objects.filter(id=group_id).first()

        if not group:
            messages.error(request, "Guruh topilmadi!")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        attendance_values = request.POST.getlist("attendance")

        for item in attendance_values:
            try:
                student_id, date_str, status = item.split("_")
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

                student = Student.objects.get(id=student_id)

                if status not in ['p', 'a', 'e']:
                    continue

                Attendance.objects.update_or_create(
                    student=student,
                    group=group,
                    date=date_obj,
                    defaults={'status': status}
                )

            except Exception as e:
                print(f"Xatolik: {e}")
                continue

        messages.success(request, "Davomat muvaffaqiyatli saqlandi!")
        return redirect(f"/admin/attendance/attendance/?group={group_id}")
