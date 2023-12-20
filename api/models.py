from django.db import models

# Create your models here.


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    vehicle_id = models.CharField(max_length=50, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Passenger(models.Model):
    id_passenger = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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


class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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


class PassangerTrip(models.Model):
    id_passanger_trip = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=255)

    def __str__(self):
        return f"Passanger on the Trip {self.id_passanger_trip}"
