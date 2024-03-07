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


class UserType(models.Model):
    id_user_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    id_city = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    identity_document = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email}) {self.type}"


class VehicleColor(models.Model):
    id_vehicle_color = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class VehicleBrand(models.Model):
    id_vehicle_brand = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class VehicleType(models.Model):
    id_vehicle_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    id_vehicle_model = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    id_vehicle = models.AutoField(primary_key=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    vehicle_brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    vehicle_color = models.ForeignKey(VehicleColor, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=10)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Conductor {self.driver_owner} tiene vehículo {self.vehicle_brand} {self.vehicle_model} - {self.license_plate}"


class Trip(models.Model):
    id_trip = models.AutoField(primary_key=True)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
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
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=255)
    seats = models.IntegerField()
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Id: {self.id_passenger_trip} Pasajero {self.passenger} en el viaje {self.trip}"
