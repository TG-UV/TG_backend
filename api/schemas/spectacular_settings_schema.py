spectacular_settings_schema = {
    'TITLE': 'API Rayo',
    'DESCRIPTION': 'Aplicación de viajes compartidos universitarios.',
    'VERSION': '1.0.0',
    'CONTACT': {'name': 'Rayo', 'email': 'rayo@correounivalle.edu.co'},
    'SERVE_INCLUDE_SCHEMA': False,
    'TAGS': [
        {'name': 'auth', 'description': 'Autenticación'},
        {'name': 'city', 'description': 'Gestión de ciudades (Admin)'},
        {'name': 'device', 'description': 'Gestión de dispositivos (Admin)'},
        {'name': 'driver', 'description': 'Endpoints para conductores'},
        {'name': 'passenger-trip', 'description': 'Gestión de reservas (Admin)'},
        {'name': 'passenger', 'description': 'Endpoints para pasajeros'},
        {'name': 'trip', 'description': 'Gestión de viajes (Admin)'},
        {'name': 'user-management', 'description': 'Gestión de usuarios (Admin)'},
        {'name': 'userType', 'description': 'Gestión de tipos de usuarios (Admin)'},
        {'name': 'users', 'description': 'Endpoints para todos los usuarios'},
        {'name': 'vehicle', 'description': 'Gestión de vehículos (Admin)'},
        {
            'name': 'vehicleBrand',
            'description': 'Gestión de marcas de vehículos (Admin)',
        },
        {
            'name': 'vehicleColor',
            'description': 'Gestión de colores de vehículos (Admin)',
        },
        {
            'name': 'vehicleModel',
            'description': 'Gestión de modelos de vehículos (Admin)',
        },
        {'name': 'vehicleType', 'description': 'Gestión de tipos de vehículos (Admin)'},
    ],
}
