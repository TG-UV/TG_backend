from django.conf import settings
import json
from datetime import date, time
from decimal import Decimal
import firebase_admin
from firebase_admin import credentials, messaging
from api.serializers.trip import ViewTripReduceSerializer
from api.models import Trip

# Configurar app de Firebase
certificate = json.loads(settings.FIREBASE_JSON)
cred = credentials.Certificate(certificate)
firebase_admin.initialize_app(cred)


# Convertir datos especiales a str
def custom_encoder(obj):
    if isinstance(obj, (date, time)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(obj)
    else:
        raise TypeError("Tipo de objeto no serializable")


# Enviar notificación a un dispositivo
def send_notification_to_device(device_token, notification, data):
    message = messaging.Message(
        notification=messaging.Notification(**notification),
        token=device_token,
        data=data,
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)


# Enviar notificación a varios dispositivos
def send_notification_to_devices(device_tokens, notification, data):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(**notification),
        tokens=device_tokens,
        data=data,
    )

    response = messaging.send_multicast(message)
    print('{0} messages were sent successfully'.format(response.success_count))
    print(device_tokens)
    print(notification)
    print(data)


# Novedades en un viaje
def send_trip_update(device_tokens, id_trip, notification):
    trip = Trip.objects.get_trip(id_trip)
    trip_serializer = ViewTripReduceSerializer(trip)

    data = {
        'notification_type': 'travel_notification',
        'additional_info': json.dumps(trip_serializer.data, default=custom_encoder),
    }

    send_notification_to_devices(device_tokens, notification, data)


# Un pasajero ha reservado
def send_new_reservation(device_tokens, id_trip):
    notification = {
        'title': 'Solicitud de cupo',
        'body': 'Un pasajero ha solicitado cupo en uno de tus viajes',
    }

    send_trip_update(device_tokens, id_trip, notification)


# Un pasajero ha cancelado la reserva
def send_reservation_canceled(device_tokens, id_trip):
    notification = {
        'title': 'Solicitud de cupo cancelada',
        'body': 'Un pasajero ha cancelado la solicitud de cupo en uno de tus viajes',
    }

    send_trip_update(device_tokens, id_trip, notification)


# El conductor acepta la reserva de un pasajero
def send_reservation_accepted(device_tokens, id_trip):
    notification = {
        'title': 'Cupo confirmado',
        'body': '¡El conductor ha aceptado llevarte!',
    }

    send_trip_update(device_tokens, id_trip, notification)


# El conductor rechaza la reserva de un pasajero
def send_reservation_rejected(device_tokens, id_trip):
    notification = {
        'title': 'Cupo rechazado',
        'body': 'Lastimosamente el conductor no puede llevarte',
    }

    trip = Trip.objects.get_trip(id_trip)
    trip_serializer = ViewTripReduceSerializer(trip)

    data = {
        'notification_type': 'travel_deny',
        'additional_info': json.dumps(trip_serializer.data, default=custom_encoder),
    }

    send_notification_to_devices(device_tokens, notification, data)


# El conductor ha cancelado el viaje
def send_trip_canceled(device_tokens, trip_dict):
    notification = {
        'title': 'Viaje cancelado',
        'body': 'Lastimosamente el conductor ha cancelado el viaje',
    }

    data = {
        'notification_type': 'travel_canceled',
        'additional_info': json.dumps(trip_dict, default=custom_encoder),
    }

    send_notification_to_devices(device_tokens, notification, data)
