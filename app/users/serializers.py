import phonenumbers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'salary', 'email', 'role', 'password', 'confirm_password')
        # extra_kwargs = {'phone_number': {'validators': []}

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)
        # salary = attrs.get('salary', None)

        if password != confirm_password:
            raise ValidationError({
                'success': False,
                'message': 'Passwords do not match',
            })

        if password:
            validate_password(password)

        # if salary.isalnum():
        #     raise ValidationError({'salary': 'Salary is invalid'})

        return attrs

    def validate_phone_number(self, phone_number):
        if not phone_number:
            raise ValidationError({
                'success': False,
                'message': "Phone number is required"
            })

        if phone_number and User.objects.filter(phone_number=phone_number).exists():
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

    def to_representation(self, instance):
        data = super(CreateUserSerializer, self).to_representation(instance)
        data.update(instance.get_tokens())
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

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

        if not phone_number or not password:
            raise ValidationError({
                'success': False,
                'message': "Phone number and password are required"
            })

        user = authenticate(request=self.context.get('request'), phone_number=phone_number, password=password)

        if user is None:
            raise ValidationError({
                'success': False,
                'message': "Username or password is incorrect"
            })

        self.user = user
        data = super().validate(attrs)
        data['user'] = dict[
            'id': self.user.id,
            'full_name': user.full_name
        ]
        return data
