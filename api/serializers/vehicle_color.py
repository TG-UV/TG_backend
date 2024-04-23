from rest_framework import serializers
from api.models import VehicleColor


class VehicleColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleColor
        fields = '__all__'
        read_only_fields = ('id_vehicle_color',)
