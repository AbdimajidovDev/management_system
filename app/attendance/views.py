from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from datetime import datetime
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from app.users.models import User
from app.users.utility import IsTeacher, IsAdminOrSuperAdmin
from .serializers import AttendanceSerializer
# from .models import Attendance, Student, Group
from .models import Attendance
from app.groups.models import Group
from app.students.models import Student



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


def save_attendance_matrix(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        if not group_id:
            return HttpResponseBadRequest("Guruh ID topilmadi.")

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return HttpResponseBadRequest("Bunday guruh mavjud emas.")

        selected = request.POST.getlist('attendance')  # ['1_2025-07-08_p', '2_2025-07-08_a', ...]

        Attendance.objects.filter(group=group).delete()

        for item in selected:
            student_id, date_str, status = item.split('_')
            student = Student.objects.get(id=student_id)
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            Attendance.objects.create(
                student=student,
                group=group,
                date=date,
                status=status
            )
        print(group.name, group_id)

        return redirect(f"/admin/attendance/attendance/?group_id={group_id}")

    return HttpResponseBadRequest("Faqat POST so‘rovlarga ruxsat bor.")
