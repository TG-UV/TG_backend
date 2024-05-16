import string
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from .custom_validators import (
    validate_date_of_birth,
    validate_lowercase_email,
    validate_identity_document,
    validate_phone_number,
    validate_seats,
    validate_fare,
    validate_latitude,
    validate_longitude,
    validate_license_plate,
)

from .custom_managers.passenger_trip import Passenger_TripManager
from .custom_managers.trip import TripManager
from .custom_managers.user import UserManager
from .custom_managers.vehicle import VehicleManager


class UserType(models.Model):
    id_user_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    id_city = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, validators=[validate_lowercase_email])
    identity_document = models.CharField(
        max_length=10, validators=[validate_identity_document]
    )
    phone_number = models.CharField(max_length=10, validators=[validate_phone_number])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(validators=[validate_date_of_birth])
    registration_date = models.DateTimeField(auto_now_add=True)
    residence_city = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'identity_document',
        'phone_number',
        'first_name',
        'last_name',
        'date_of_birth',
        'residence_city',
        'type',
    ]

    def save(self, *args, **kwargs):
        # Da formato a algunos campos antes de guardar.
        self.first_name = string.capwords(self.first_name)
        self.last_name = string.capwords(self.last_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}) {self.type}"


class VehicleColor(models.Model):
    id_vehicle_color = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class VehicleBrand(models.Model):
    id_vehicle_brand = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class VehicleType(models.Model):
    id_vehicle_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    id_vehicle_model = models.AutoField(primary_key=True)
    name = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id_vehicle = models.AutoField(primary_key=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    vehicle_brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    vehicle_color = models.ForeignKey(VehicleColor, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=7, validators=[validate_license_plate])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = VehicleManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['license_plate', 'owner'], name='license_plate_owner_unique'
            )  # Valida que un conductor no añada un mismo vehículo varias veces.
        ]

    def save(self, *args, **kwargs):
        # Convierte la placa a mayúsculas antes de guardar.
        self.license_plate = self.license_plate.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vehículo {self.vehicle_brand} {self.vehicle_model} - {self.license_plate} registrado por {self.owner}"


class Trip(models.Model):
    id_trip = models.AutoField(primary_key=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    starting_point_lat = models.DecimalField(
        max_digits=8, decimal_places=6, validators=[validate_latitude]
    )
    starting_point_long = models.DecimalField(
        max_digits=9, decimal_places=6, validators=[validate_longitude]
    )
    arrival_point_lat = models.DecimalField(
        max_digits=8, decimal_places=6, validators=[validate_latitude]
    )
    arrival_point_long = models.DecimalField(
        max_digits=9, decimal_places=6, validators=[validate_longitude]
    )
    seats = models.IntegerField(validators=[validate_seats])
    fare = models.IntegerField(validators=[validate_fare])
    current_trip = models.BooleanField(default=False)

    objects = TripManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['start_date', 'start_time', 'driver'],
                name='start_datetime_driver_unique',
            )  # Valida que un conductor no cree varios viajes con la misma fecha y hora.
        ]

    def __str__(self):
        return f"Trip #{self.id_trip}"


class Passenger_Trip(models.Model):
    id_passenger_trip = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_point_lat = models.DecimalField(
        max_digits=8, decimal_places=6, validators=[validate_latitude]
    )
    pickup_point_long = models.DecimalField(
        max_digits=9, decimal_places=6, validators=[validate_longitude]
    )
    seats = models.IntegerField(validators=[validate_seats])
    is_confirmed = models.BooleanField(default=False)

    objects = Passenger_TripManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['passenger', 'trip'], name='passenger_trip_unique'
            )  # Valida que un pasajero solo aparezca una vez en un viaje.
        ]

    def __str__(self):
        return f"Id: {self.id_passenger_trip} Pasajero {self.passenger} en el viaje {self.trip}"


class Device(models.Model):
    id_device = models.TextField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispositivo: {self.id_device} Usuario {self.user}"
