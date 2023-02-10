from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, \
                    UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages

def user_login(request):
    '''Vista para el manejo del login'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(request.POST) # TODO: eliminar esta linea
        if form.is_valid():
            cd = form.cleaned_data
            # authenticate() -> revisa las credenciales y retorna un objeto User 
            # si son correctas.
            user = authenticate(
                        request,
                        username=cd['username'],
                        password=cd['password'],
                    )
            
            if user is not None:
                if user.is_active:
                    # login() -> Establece al usuario en la sesion actual
                    login(request, user)
                    return HttpResponse('Autenticacion exitosa')
                else:
                    return HttpResponse('Cuenta esta deshabilitada')
            else:
                return HttpResponse('Login invalido')

    else:
        form = LoginForm()
    
    return render(
        request,
        'account/login.html',
        {'form': form},
    )

@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )

def register(request):
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
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )