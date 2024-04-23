from rest_framework import serializers
from api.models import VehicleModel


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = '__all__'
        read_only_fields = ('id_vehicle_model',)
