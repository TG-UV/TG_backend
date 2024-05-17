from django.test import TestCase
from api.models import (
    UserType,
    City,
    User,
    VehicleColor,
    VehicleBrand,
    VehicleType,
    VehicleModel,
    Vehicle,
)

# Comando para ejecutar las pruebas: py manage.py test api.tests.models


# Pruebas de los modelos
class BaseTestCase(TestCase):
    def setUp(self):
        self.city = City.objects.create(name='Cali')

        self.user_type = UserType.objects.create(name='Conductor')

        self.user = User.objects.create(
            email='m.camila@correounivalle.edu.co',
            identity_document='1002100443',
            phone_number='3002451922',
            first_name='maría cAmIla',
            last_name='aRIas',
            date_of_birth='2000-04-10',
            residence_city=self.city,
            type=self.user_type,
        )

        self.color = VehicleColor.objects.create(name='Negro')

        self.brand = VehicleBrand.objects.create(name='Mazda')

        self.type = VehicleType.objects.create(name='Carro')

        self.model = VehicleModel.objects.create(name='2022')

        self.vehicle = Vehicle.objects.create(
            vehicle_type=self.type,
            vehicle_brand=self.brand,
            vehicle_model=self.model,
            vehicle_color=self.color,
            license_plate='ABC-123',
            owner=self.user,
        )


class UserTypeTestCase(BaseTestCase):
    def test_name(self):
        self.assertEqual(self.user_type.name, 'Conductor')


class CityTestCase(BaseTestCase):
    def test_name(self):
        self.assertEqual(self.city.name, 'Cali')


class UserTestCase(BaseTestCase):
    def test_user_attributes(self):
        expected_data = {
            'email': 'm.camila@correounivalle.edu.co',
            'identity_document': '1002100443',
            'phone_number': '3002451922',
            'first_name': 'María Camila',
            'last_name': 'Arias',
            'date_of_birth': '2000-04-10',
            'residence_city': 'Cali',
            'type': 'Conductor',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }

        actual_data = {
            'email': self.user.email,
            'identity_document': self.user.identity_document,
            'phone_number': self.user.phone_number,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'date_of_birth': str(self.user.date_of_birth),
            'residence_city': self.user.residence_city.name,
            'type': self.user.type.name,
            'is_active': self.user.is_active,
            'is_staff': self.user.is_staff,
            'is_superuser': self.user.is_superuser,
        }

        self.assertEqual(expected_data, actual_data)


class VehicleColorTestCase(BaseTestCase):
    def test_name(self):
        self.assertEqual(self.color.name, 'Negro')


class VehicleBrandTestCase(BaseTestCase):
    def test_name(self):
        self.assertEqual(self.brand.name, 'Mazda')


class VehicleTypeTestCase(BaseTestCase):
    def test_name(self):
        self.assertEqual(self.type.name, 'Carro')


class VehicleModelTestCase(BaseTestCase):
    def test_name(self):
        self.assertEqual(self.model.name, '2022')


class VehicleTestCase(BaseTestCase):
    def test_vehicle_attributes(self):
        expected_data = {
            'license_plate': 'ABC-123',
            'vehicle_type': 'Carro',
            'vehicle_brand': 'Mazda',
            'vehicle_model': '2022',
            'vehicle_color': 'Negro',
            'owner': 'María Camila',
        }

        actual_data = {
            'license_plate': self.vehicle.license_plate,
            'vehicle_type': self.vehicle.vehicle_type.name,
            'vehicle_brand': self.vehicle.vehicle_brand.name,
            'vehicle_model': self.vehicle.vehicle_model.name,
            'vehicle_color': self.vehicle.vehicle_color.name,
            'owner': self.vehicle.owner.first_name,
        }

        self.assertEqual(expected_data, actual_data)
