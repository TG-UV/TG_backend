from django.contrib import admin
from .models import Driver, Passenger, VehicleColor, VehicleBrand, VehicleType, VehicleModel, Vehicle, Admin, Trip, PassangerTrip

# Register your models here.
admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(VehicleColor)
admin.site.register(VehicleBrand)
admin.site.register(VehicleType)
admin.site.register(VehicleModel)
admin.site.register(Vehicle)
admin.site.register(Admin)
admin.site.register(Trip)
admin.site.register(PassangerTrip)