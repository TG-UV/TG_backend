from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('Se requiere un email')

        if not password:
            raise ValueError('Se requiere una contraseña')

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    identity_document = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'identity_document',
        'phone_number',
        'first_name',
        'last_name',
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Driver(models.Model):
    id_driver = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Conductor {self.id_driver} es {self.user_id}"


class Passenger(models.Model):
    id_passenger = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pasajero {self.id_passenger} es {self.user_id}"


class VehicleColor(models.Model):
    id_vehicle_color = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class VehicleBrand(models.Model):
    id_vehicle_brand = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class VehicleType(models.Model):
    id_vehicle_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    id_vehicle_model = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id_vehicle = models.AutoField(primary_key=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    vehicle_brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    vehicle_color = models.ForeignKey(VehicleColor, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.vehicle_brand} {self.vehicle_model} - {self.license_plate}"


class Driver_Vehicle(models.Model):
    id_driver_vehicle = models.AutoField(primary_key=True)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return f"Conductor {self.driver_id} tiene vehículo {self.vehicle_id}"


class Trip(models.Model):
    id_trip = models.AutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    starting_point = models.CharField(max_length=255)
    arrival_point = models.CharField(max_length=255)
    seats = models.IntegerField()
    fare = models.IntegerField()
    current_trip = models.BooleanField(default=False)

    def __str__(self):
        return f"Trip #{self.id_trip}"


class Passenger_Trip(models.Model):
    id_passenger_trip = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Id: {self.id_passenger_trip} Pasajero {self.passenger} en el viaje {self.trip}"
