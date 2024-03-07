from django.contrib import admin
from .models import (
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
)

# Register your models here.
admin.site.register(UserType)
admin.site.register(City)
admin.site.register(User)
admin.site.register(VehicleColor)
admin.site.register(VehicleBrand)
admin.site.register(VehicleType)
admin.site.register(VehicleModel)
admin.site.register(Vehicle)
admin.site.register(Trip)
admin.site.register(Passenger_Trip)
