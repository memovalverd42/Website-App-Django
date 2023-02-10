# Django imports
from django import forms
from django.contrib.auth.models import User
# Local Django
from .models import Profile

class LoginForm(forms.Form):
    '''Formulario para iniciar sesion'''
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    '''Formulario para registrar un usuario'''
    password = forms.CharField(
                    label='Password',
                    widget=forms.PasswordInput,
                )
    password2 = forms.CharField(
                    label='Repeat password',
                    widget=forms.PasswordInput,
                )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        '''Metodo para validar los passwords'''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

    def clean_email(self):
        '''Metodo para validar el correo'''
        data = self.cleaned_data['email']
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
        qs = User.objects.exclude(id=self.instance.id)\
                         .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('El correo ya está en uso.')
        return data

class ProfileEditForm(forms.ModelForm):
    '''Formulario para editar datos de un perfil'''
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']