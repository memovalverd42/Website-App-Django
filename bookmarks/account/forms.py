# Django imports
from django import forms
from django.contrib.auth.models import User
# Local Django
from .models import Profile

class LoginForm(forms.Form):
    '''Formulario para iniciar sesion'''
    username = forms.CharField()
    # Campo con widget PasswordInput para que renderise
    # el imput en el HTML como password input
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    '''Formulario para registrar un usuario'''
    # Campos custom para el registro
    password = forms.CharField(
                    label='Password',
                    widget=forms.PasswordInput,
                )
    password2 = forms.CharField(
                    label='Repeat password',
                    widget=forms.PasswordInput,
                )

    class Meta:
        # Modelo en el que se basa el formulario
        model = User
        # Campos del modelo que tendrá el formulario
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        '''Metodo para validar los passwords'''
        # Guardamos el diccionario de los datos obtenidos
        cd = self.cleaned_data
        # Si las passwords son diferentes se lanza un error de validacion
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        # Si todo sale bien se retorna el password
        return cd['password2']

    def clean_email(self):
        '''Metodo para validar el correo'''
        # Guardamos el correo
        data = self.cleaned_data['email']
        # Corroborar si existe usuario
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('El correo ya está en uso.')
        return data

class UserEditForm(forms.ModelForm):
    '''Formulario para editar datos de un User'''
    class Meta:
        model = User   
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        # queryset con el correo del usuario
        qs = User.objects.exclude(id=self.instance.id)\
                         .filter(email=data)
        # Si ya existe ese correo se laza un error
        if qs.exists():
            raise forms.ValidationError('El correo ya está en uso.')
        return data


class ProfileEditForm(forms.ModelForm):
    '''Formulario para editar datos de un perfil'''
    class Meta:
        model = Profile
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'format': '%d/%m/%Y'}),
        }
        fields = ['date_of_birth', 'photo']