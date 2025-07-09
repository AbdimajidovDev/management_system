from rest_framework import serializers
from .models import *


class TeacherSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSalary
        fields = '__all__'
        read_only_fields = ('id',)
