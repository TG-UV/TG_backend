from rest_framework import serializers
from api.models import UserType


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'
        read_only_fields = ('id_user_type',)
