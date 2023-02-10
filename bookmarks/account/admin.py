from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Panel de administrador para los perfiles'''
    # Lista de campos de información para mostrar
    list_display = ['user', 'date_of_birth', 'photo']
    # Lista de campos que se muestran como enlances
    raw_id_fields = ['user']