'''import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("../google-services.json")
firebase_admin.initialize_app(cred)


# Método para enviar una notificación a un dispositivo específico
def send_notification_to_device(device_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=device_token,
    )
    response = messaging.send(message)
    print("Successfully sent message:", response)
'''