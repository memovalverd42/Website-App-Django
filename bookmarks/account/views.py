# Django imports
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Local Django
from .forms import LoginForm, UserRegistrationForm, \
                    UserEditForm, ProfileEditForm
from .models import Profile

def user_login(request):
    '''Vista para el manejo del login'''
    if request.method == 'POST':
        # Creacion de instancia de formulario con el request
        form = LoginForm(request.POST)
        if form.is_valid():
            # Si se cumple la validacion se obtiene diccionario con datos
            cd = form.cleaned_data
            # authenticate() -> revisa las credenciales y retorna un objeto User 
            # si son correctas.
            user = authenticate(
                        request,
                        username=cd['username'],
                        password=cd['password'],
                    )
            
            # Si la utenticacion fue exitosa...
            if user is not None:
                if user.is_active:
                    # login() -> Establece al usuario en la sesion actual
                    login(request, user)
                    return HttpResponse('Autenticacion exitosa')
                else:
                    return HttpResponse('Cuenta esta deshabilitada')
            else:
                return HttpResponse('Login invalido')

    # En caso de que apenas se vaya a hacer un llenado del form
    else:
        # Se genera una instancia del formulario para retornar
        form = LoginForm()
    
    return render(
        request,
        'account/login.html',
        {'form': form},
    )

@login_required
def dashboard(request):
    '''Vista para manejo del dashboard'''
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )

def register(request):
    '''Vista para el registro de usuarios'''
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Crear una instancia de usuario sin guardar en la DB
            new_user = user_form.save(commit=False)
            # Agregamos el password que escribio
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            # Guardamos al usuario en la db
            new_user.save()

            # Creacion de un perfil
            Profile.objects.create(user=new_user)

            return render(
                request,
                'account/register_done.html',
                {'new_user': new_user}
            )
    
    else:
        user_form = UserRegistrationForm()
    
    return render(
        request,
        'account/register.html',
        {'user_form': user_form}
    )

@login_required
def edit(request):
    '''Vista para editar perfil de usuario'''
    if request.method == 'POST':
        user_form = UserEditForm(
                        instance=request.user,
                        data=request.POST
                    )
        profile_form = ProfileEditForm(
                            instance=request.user.profile,
                            data=request.POST,
                            files=request.FILES
                        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated succesfully')
        
        else:
            messages.error(request, 'Error updating yout profile')
    
    else:
        user_form = UserEditForm(instance=request.user)
        user_profile = Profile.objects.filter(user=request.user)
        if not user_profile.exists():
            Profile.objects.create(user=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )