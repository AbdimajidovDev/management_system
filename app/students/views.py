from django.shortcuts import render
from django.views import View
from rest_framework import viewsets

from app.students.models import Student
from app.students.serializers import StudentSerializer
from app.users.utility import IsAdmin, IsSuperAdmin


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin | IsSuperAdmin]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

