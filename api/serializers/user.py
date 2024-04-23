from rest_framework import serializers
from djoser.serializers import (
    UserSerializer,
    UserCreateSerializer,
    UsernameSerializer,
    CurrentPasswordSerializer,
)
from api import error_messages
from api.custom_validators import validate_email_domain, ALLOWED_EMAIL_DOMAIN
from api.models import User


class ExtendedUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id_user',
            'email',
            'identity_document',
            'phone_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'password',
            'registration_date',
            'residence_city',
            'type',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser',
        )
        read_only_fields = (
            'id_user',
            'registration_date',
            'last_login',
            'is_staff',
            'is_superuser',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }  # Para que no se pueda ver.

    def create(self, validated_data):
        user_type = validated_data['type']

        if user_type.name == 'Admin':
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        user_type = validated_data.get('type', instance.type)
        password = validated_data.pop('password', None)

        if user_type.name == 'Admin':
            validated_data['is_staff'] = True
            validated_data['is_superuser'] = True
        else:
            validated_data['is_staff'] = False
            validated_data['is_superuser'] = False

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CustomUserCreateSerializer(UserCreateSerializer):

    def validate(self, attrs):
        email = attrs['email']
        user_type = attrs['type']
        allowed_types = ['Conductor', 'Pasajero']
        errors = {}

        # Validaciones de Django.
        attrs = super().validate(attrs)

        # Valida que solo se puedan registrar Conductores o Pasajeros.
        if user_type.name not in allowed_types:
            errors['type'] = error_messages.INVALID_USER_TYPE

        # Valida el dominio del correo.
        if not email.endswith(ALLOWED_EMAIL_DOMAIN):
            errors['email'] = error_messages.EMAIL_DOMAIN_NOT_ALLOWED

        if not errors:
            return attrs
        else:
            raise serializers.ValidationError(errors)


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'id_user',
            'email',
            'identity_document',
            'phone_number',
            'first_name',
            'last_name',
            'date_of_birth',
            'residence_city',
            'type',
            'is_active',
        )
        read_only_fields = ('id_user', 'email', 'type')


class ViewUserSerializer(CustomUserSerializer):
    residence_city = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_residence_city(self, obj):
        return obj.residence_city.name if obj.residence_city else None

    def get_type(self, obj):
        return obj.type.name if obj.type else None


class ViewUserReduceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'phone_number',
            'first_name',
            'last_name',
        )
        read_only_fields = fields


class CustomSetUsernameSerializer(UsernameSerializer, CurrentPasswordSerializer):
    class Meta:
        model = User
        fields = ('email', 'current_password')

    def validate(self, attrs):
        email = attrs['email']

        # Validaciones de Django.
        attrs = super().validate(attrs)

        # Valida el dominio del correo.
        validate_email_domain(email)

        return attrs
