from django.core.exceptions import ValidationError
from datetime import datetime


def validate_date_of_birth(date_of_birth):
    current_date = datetime.now().date()

    if not date_of_birth <= current_date:
        raise ValidationError(
            'La fecha de nacimiento no puede ser mayor que la fecha actual.'
        )
