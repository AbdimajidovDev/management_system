import phonenumbers
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.students.models import Student
from app.users.models import User


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'full_name', 'phone_number', 'group')
        extra_kwargs = {'phone_number': {'validators': []}}

    def validate_phone_number(self, phone_number):
        if not phone_number:
            data = {
                'success': False,
                'message': "Phone number is required"
            }
            raise ValidationError(data)

        if phone_number and (Student.objects.filter(phone_number=phone_number).exists() or User.objects.filter(phone_number=phone_number).exists()):
            data = {
                'status': False,
                'message': "Phone number is already registered"
            }
            raise ValidationError(data)

        try:
            parsed_number = phonenumbers.parse(phone_number)
            if not phonenumbers.is_valid_number(parsed_number):
                data = {
                    'success': False,
                    'message': "Phone number is invalid"
                }
                raise ValidationError(data)
        except phonenumbers.NumberParseException:
            data = {
                'success': False,
                'message': "Your phone number is in the wrong format.. (Correct format: +998xxxxxxxxx)"
            }
            raise ValidationError(data)
        return phone_number
