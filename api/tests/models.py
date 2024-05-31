from decimal import Decimal
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
    Trip,
    Passenger_Trip,
    Device,
)

# Comando para ejecutar las pruebas: py manage.py test api.tests.models


# Pruebas de los modelos
class BaseTestCase(TestCase):
    """
    Pruebas para probar la creación y consulta de objetos de cada modelo.
    Sirven para comprobar si los objetos se comportan de acuerdo a lo esperado,
    si se aplican los formatos a los campos antes de guardar y si se obtienen 
    los tipos de datos definidos al crear los modelos.
    """

    def setUp(self):
        self.city = City.objects.create(name='Cali')

        self.user_type = UserType.objects.create(name='Conductor')
        self.passenger_user_type = UserType.objects.create(name='Pasajero')

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

        self.passenger = User.objects.create(
            email='luis.ruiz@correounivalle.edu.co',
            identity_document='29843482',
            phone_number='3224323200',
            first_name='Luis',
            last_name='Ruíz',
            date_of_birth='2001-02-08',
            residence_city=self.city,
            type=self.passenger_user_type,
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

        self.trip = Trip.objects.create(
            driver=self.user,
            vehicle=self.vehicle,
            start_date='2024-06-06',
            start_time='14:45:00',
            starting_point_lat=Decimal('3.375462'),
            starting_point_long=Decimal('-76.533166'),
            arrival_point_lat=Decimal('3.451700'),
            arrival_point_long=Decimal('-76.536400'),
            seats=4,
            fare=3200,
        )

        self.passenger_trip = Passenger_Trip.objects.create(
            trip=self.trip,
            passenger=self.passenger,
            pickup_point_lat=Decimal('3.375462'),
            pickup_point_long=Decimal('-76.533166'),
            seats=2,
        )

        self.device = Device.objects.create(
            id_device='fFM2mx0hTNa7TKSgpFmlxw:APA91bFIhAXnKkGSDTSlvVMUk59YpJaJ9jOBhEC3MCiVXVgpIp5DSZp5',
            user=self.passenger,
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
            'date_of_birth': self.user.date_of_birth,
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


class TripTestCase(BaseTestCase):
    def test_trip_attributes(self):
        expected_data = {
            'start_date': '2024-06-06',
            'start_time': '14:45:00',
            'starting_point_lat': Decimal('3.375462'),
            'starting_point_long': Decimal('-76.533166'),
            'arrival_point_lat': Decimal('3.451700'),
            'arrival_point_long': Decimal('-76.536400'),
            'seats': 4,
            'fare': 3200,
            'current_trip': False,
            'driver': 'María Camila',
            'vehicle': 'ABC-123',
        }

        actual_data = {
            'start_date': self.trip.start_date,
            'start_time': self.trip.start_time,
            'starting_point_lat': self.trip.starting_point_lat,
            'starting_point_long': self.trip.starting_point_long,
            'arrival_point_lat': self.trip.arrival_point_lat,
            'arrival_point_long': self.trip.arrival_point_long,
            'seats': self.trip.seats,
            'fare': self.trip.fare,
            'current_trip': self.trip.current_trip,
            'driver': self.trip.driver.first_name,
            'vehicle': self.trip.vehicle.license_plate,
        }

        self.assertEqual(expected_data, actual_data)


class Passenger_TripTestCase(BaseTestCase):
    def test_passenger_trip_attributes(self):
        expected_data = {
            'pickup_point_lat': Decimal('3.375462'),
            'pickup_point_long': Decimal('-76.533166'),
            'seats': 2,
            'is_confirmed': False,
            'trip': 3200,
            'passenger': 'Luis',
        }

        actual_data = {
            'pickup_point_lat': self.passenger_trip.pickup_point_lat,
            'pickup_point_long': self.passenger_trip.pickup_point_long,
            'seats': self.passenger_trip.seats,
            'is_confirmed': self.passenger_trip.is_confirmed,
            'trip': self.passenger_trip.trip.fare,
            'passenger': self.passenger_trip.passenger.first_name,
        }

        self.assertEqual(expected_data, actual_data)


class DeviceTestCase(BaseTestCase):
    def test_id_device(self):
        self.assertEqual(
            self.device.id_device,
            'fFM2mx0hTNa7TKSgpFmlxw:APA91bFIhAXnKkGSDTSlvVMUk59YpJaJ9jOBhEC3MCiVXVgpIp5DSZp5',
        )

    def test_user(self):
        self.assertEqual(self.device.user.first_name, 'Luis')
