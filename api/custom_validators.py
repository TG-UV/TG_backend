import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from api import error_messages
from decimal import Decimal


ALLOWED_EMAIL_DOMAIN = '@correounivalle.edu.co'


def validate_date_of_birth(date_of_birth):
    current_date = timezone.now().date()

    if date_of_birth > current_date:
        raise ValidationError(error_messages.INVALID_DATE_OF_BIRTH)


def validate_lowercase_email(email):
    if not email.islower():
        raise ValidationError(error_messages.EMAIL_MUST_BE_IN_LOWERCASE)


def validate_numbers_only(string, error):
    if not string.isdigit():
        raise ValidationError(error)


def validate_identity_document(identity_document):
    validate_numbers_only(identity_document, error_messages.INVALID_IDENTITY_DOCUMENT)


def validate_phone_number(phone_number):
    validate_numbers_only(phone_number, error_messages.INVALID_PHONE_NUMBER)

    if len(phone_number) != 10:
        raise ValidationError(error_messages.WRONG_PHONE_NUMBER_LENGTH)


def validate_positive_integer(number, error):
    if number < 0:
        raise ValidationError(error)


def validate_seats(seats):
    validate_positive_integer(seats, error_messages.NEGATIVE_SEATS)


def validate_fare(fare):
    validate_positive_integer(fare, error_messages.NEGATIVE_FARE)


def validate_driver(user):
    if user.type.name != 'Conductor':
        raise ValidationError({"driver": [error_messages.USER_MUST_BE_A_DRIVER]})


def validate_passenger(user):
    if user.type.name != 'Pasajero':
        raise ValidationError({"passenger": [error_messages.USER_MUST_BE_A_PASSENGER]})


def validate_vehicle_owner(driver, vehicle):
    if driver.id_user != vehicle.owner.id_user:
        raise ValidationError(
            {
                "vehicle": [error_messages.VEHICLE_DOES_NOT_BELONG_TO_THE_DRIVER],
                "driver": [error_messages.VEHICLE_DOES_NOT_BELONG_TO_THE_DRIVER],
            }
        )


def validate_email_domain(email):
    if not email.endswith(ALLOWED_EMAIL_DOMAIN):
        raise ValidationError(
            {
                'new_email': error_messages.EMAIL_DOMAIN_NOT_ALLOWED,
            }
        )


def validate_latitude(latitude):
    if latitude > Decimal('90.000000') or latitude < Decimal('-90.000000'):
        raise ValidationError(error_messages.INVALID_LATITUDE)


def validate_longitude(longitude):
    if longitude > Decimal('180.000000') or longitude < Decimal('-180.000000'):
        raise ValidationError(error_messages.INVALID_LONGITUDE)


def validate_license_plate(license_plate):
    pattern = r'^[A-Za-z]{3}-\d{3}$'
    if not re.match(pattern, license_plate):
        raise ValidationError(error_messages.INVALID_LICENSE_PLATE)
