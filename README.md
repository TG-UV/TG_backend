# TG_backend

Django backend

## Configuración inicial:

Instalar virutalenv:
`pip install virtualenv`

Descargar repositorio.

En la carpeta del repositorio ejecutar:

Crear el entorno virtual:
`virtualenv venv`

Activar el entorno virtual:
`venv\Scripts\activate`

Luego, dentro del venv ejecutar:
`pip install -r requirements.txt`

Pegar el archivo .env en la carpeta raíz.

### Para correr la aplicación:

En Visual Studio Code presioanr F1> Seleccionar interprete > venv.

Luego, dentro del venv ejecutar:
`python manage.py migrate`

Luego:
`python manage.py runserver`


### Para actualizar los modelos de datos:
`python manage.py makemigrations`

Luego:
`python manage.py migrate`