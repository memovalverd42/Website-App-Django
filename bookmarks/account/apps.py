from django.apps import AppConfig

# Esto sirve para agregar el comportamiento de configuracion de la aplicacion
class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # Tipo de clave primaria que se usará para los modelos
    name = 'account'                                     # Nombre de la aplicacion