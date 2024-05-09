from django.conf import settings
import json
import firebase_admin
from firebase_admin import credentials, messaging

certificate = json.loads(settings.FIREBASE_JSON)

cred = credentials.Certificate(certificate)
firebase_admin.initialize_app(cred)


# Método para enviar una notificación a un dispositivo específico
def send_notification_to_device(device_token, notification, data):
    message = messaging.Message(
        notification=messaging.Notification(**notification),
        token=device_token,
        data=data,
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)


def send_reservation_rejected(device_token):
    notification = {
        'title': 'Cupo rechazado',
        'body': 'Lastimosamente el conductor no puede llevarte',
    }

    data = {
        'notification_type': 'travel_deny',
        'additional_info': '',
    }

    send_notification_to_device(device_token, notification, data)


def send_welcome(device_token):
    notification = {
        'title': 'Bienvenido',
        'body': 'Disfruta de nuestra app',
    }

    data = {
        'notification_type': 'current_travel',
        'additional_info': json.dumps({
            'id_trip': '1',
            'start_date': '2024-05-08',
            'start_time': '16:00:00',
            'starting_point': {
                'lat': '3.375462',
                'long': '-76.533166',
            },
            'arrival_point': {
                'lat': '3.375462',
                'long': '-76.533166',
            },
            'seats': '4',
            'fare': '4000',
        }),
    }

    print(data)

    send_notification_to_device(device_token, notification, data)
