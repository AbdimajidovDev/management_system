import phonenumbers
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    try:
        parsed_number = phonenumbers.parse(value)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError(message="Phone number is invalid")
    except phonenumbers.NumberParseException:
        raise ValidationError(message="Your phone number is in the wrong format.. (Correct format: +998xxxxxxxxx)")
    return value
