import phonenumbers
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from app.attendance.models import Attendance
from app.students.models import Student, StudentGroup
from app.users.models import User


class StudentSerializer(serializers.ModelSerializer):
    # attendance_stats = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'full_name', 'phone_number', 'parents_phone_number')
        extra_kwargs = {'phone_number': {'validators': []}}

    def validate(self, attrs):
        print('attrs', attrs)
        parents_phone_number = attrs.get('parents_phone_number')
        print('phoooooone', parents_phone_number)

        if not parents_phone_number:
            raise ValidationError({
                'success': False,
                'message': "Phone number is required"
            })

        if [parents_phone_number] and (Student.objects.filter(phone_number=[parents_phone_number]).exists() or User.objects.filter(phone_number=parents_phone_number).exists()):
            raise ValidationError( {
                'status': False,
                'message': "Phone number is already registered"
            })

        try:
            parsed_number = phonenumbers.parse(parents_phone_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError({
                    'success': False,
                    'message': "Phone number is invalid"
                })
        except phonenumbers.NumberParseException:
            raise ValidationError({
                'success': False,
                'message': "Your phone number is in the wrong format.. (Correct format: +998xxxxxxxxx)"
            })
        return attrs


    def validate_phone_number(self, phone_number):
        print('phone_number: ', phone_number)
        if not phone_number:
            raise ValidationError({
                'success': False,
                'message': "Phone number is required"
            })

        if phone_number and (Student.objects.filter(phone_number=phone_number).exists() or User.objects.filter(phone_number=phone_number).exists()):
            raise ValidationError({
                'status': False,
                'message': "Phone number is already registered"
            })

        try:
            parsed_number = phonenumbers.parse(phone_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError({
                    'success': False,
                    'message': "Phone number is invalid"
                })
        except phonenumbers.NumberParseException:
            raise ValidationError({
                'success': False,
                'message': "Your phone number is in the wrong format.. (Correct format: +998xxxxxxxxx)"
            })
        return phone_number


class StudentGroupSerializer(serializers.Serializer):
    class Meta:
        model = StudentGroup
        fields = ('student', 'group')
        read_only_fields = ('id',)
