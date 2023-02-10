from django.db import models
from django.conf import settings

class Profile(models.Model):
    '''Modelo para los perfiles de usuario'''
    # Se crea campo con una relacion uno a uno con el usuario
    user = models.OneToOneField(
                # Para configurar que se pueda usar con el
                # modelo predeterminado o con uno custom
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            )
    
    date_of_birth = models.DateField(blank=True, null=True,)
    # date_of_birth = models.DateField(null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self) -> str:
        return f'Perfil de {self.user.username}'