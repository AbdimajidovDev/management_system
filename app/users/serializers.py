import phonenumbers
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'role', 'password', 'confirm_password')
        # extra_kwargs = {'phone_number': {'validators': []}

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)
        # first_name = attrs.get('first_name', None)
        # last_name = attrs.get('last_name', None)

        if password != confirm_password:
            data = {
                'success': False,
                'message': 'Passwords do not match',
            }
            raise ValidationError(data)

        if password:
            validate_password(password)

        return attrs

    def validate_phone_number(self, phone_number):
        if not phone_number:
            data = {
                'success': False,
                'message': "Phone number is required"
            }
            raise ValidationError(data)

        if phone_number and User.objects.filter(phone_number=phone_number).exists():
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

