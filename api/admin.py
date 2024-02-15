from django.contrib import admin
from .models import (
    User,
    Driver,
    Passenger,
    VehicleColor,
    VehicleBrand,
    VehicleType,
    VehicleModel,
    Vehicle,
    Driver_Vehicle,
    Trip,
    Passenger_Trip,
)

# Register your models here.
admin.site.register(User)
admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(VehicleColor)
admin.site.register(VehicleBrand)
admin.site.register(VehicleType)
admin.site.register(VehicleModel)
admin.site.register(Vehicle)
admin.site.register(Driver_Vehicle)
admin.site.register(Trip)
admin.site.register(Passenger_Trip)
