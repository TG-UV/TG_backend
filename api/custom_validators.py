from django.core.exceptions import ValidationError
from datetime import datetime
from api import error_messages


def validate_date_of_birth(date_of_birth):
    current_date = datetime.now().date()

    if date_of_birth > current_date:
        raise ValidationError(error_messages.INVALID_DATE_OF_BIRTH)
