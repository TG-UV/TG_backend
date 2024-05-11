from django.db import models


class VehicleManager(models.Manager):
    def base_query(self):
        queryset = self.get_queryset()
        return queryset.select_related(
            'vehicle_type',
            'vehicle_brand',
            'vehicle_model',
            'vehicle_color',
        ).only(
            'id_vehicle',
            'vehicle_type',
            'vehicle_brand',
            'vehicle_model',
            'vehicle_color',
            'license_plate',
        )

    def get_vehicle(self, id_vehicle, owner):
        return self.base_query().get(id_vehicle=id_vehicle, owner=owner)

    def get_my_vehicles(self, owner):
        return self.base_query().filter(owner=owner).order_by('license_plate')
