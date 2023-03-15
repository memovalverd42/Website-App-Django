"""
Archivo para generar formas de autenticacion custom
"""
from django.contrib.auth.models import User
from account.models import Profile

def create_profile(backend, user, *args, **kwards):
    '''Crear un perfil de usuario para la autenticacion son redes sociales'''
    Profile.objects.get_or_create(user=user)

class EmailAuthBackend:
    """
    Autenticación usando el correo.
    """
    def authenticate(self, request, username=None, password=None):
        '''Metodo para autenticar con el correo'''
        try:
            # Crear instancia del usuario con el correo del username
            user = User.objects.get(email=username)
            # Comprobacion del password
            if user.check_password(password):
                return user
            return None
        # En caso de error, lanzar excepts:
        #  - Si el usuario no exciste
        #  - Si hay multiples usuarios con las mismas credenciales
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        '''Metodo para obtener usuario con id'''
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None