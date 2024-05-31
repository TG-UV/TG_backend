from django.core.exceptions import ValidationError
from django.test import TestCase
from api.custom_validators import validate_license_plate

# Comando para ejecutar las pruebas: py manage.py test api.tests.validators


class LicensePlateValidationTestCase(TestCase):
    """
    Pruebas para probar la expresión regular que válida el formato
    de la placa de un vehículo.
    """

    def test_valid_license_plate(self):
        valid_license_plates = ['ABC-123', 'XYZ-12A', 'cal-202', 'sum-32a']
        for plate in valid_license_plates:
            try:
                validate_license_plate(plate)
            except ValidationError:
                self.fail(
                    'validate_license_plate() lanzó un ValidationError para la placa '
                    + F'{plate}'
                )

    def test_invalid_license_plate(self):
        invalid_license_plates = [
            'AB-123',
            'ABCD-123',
            'ABC-1234',
            'ABC123',
            'abc-1ee',
            '213-ABC',
            'MVP-EEE',
        ]
        for plate in invalid_license_plates:
            with self.assertRaises(ValidationError):
                validate_license_plate(plate)
