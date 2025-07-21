from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from app.attendance.models import Attendance
from app.attendance.serializers import AttendanceSerializer
from app.students.models import Student, StudentGroup
from app.students.serializers import StudentSerializer, StudentGroupSerializer
from app.users.permissions import IsAdminOrSuperAdmin


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrSuperAdmin, )
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @extend_schema(responses=AttendanceSerializer(many=True))
    @action(detail=True, methods=['get'], url_path='attendance')
    def attendance(self, request, pk=None):
        student = self.get_object()
        group = student.group

        if not group:
            return Response({"detail": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

        attendances = Attendance.objects.filter(student=student, group=group)

        total = attendances.count()
        present = attendances.filter(status='p').count()
        absent = attendances.filter(status='a').count()
        percentage = round((present / total) * 100, 2) if total else 0

        serializer = AttendanceSerializer(attendances, many=True)

        return Response({
            'group_name': group.name,
            'total_classes': total,
            'present': present,
            'absent': absent,
            'attendance_percentage': percentage,
            'attendances': serializer.data
        }, status=status.HTTP_200_OK)

@extend_schema(tags=['student-payment'], responses=StudentGroupSerializer(many=True))
class StudentGroupViewSet(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrSuperAdmin, )
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
