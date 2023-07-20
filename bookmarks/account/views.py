# Django imports
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
# Local Django
from .forms import LoginForm, UserRegistrationForm, \
                    UserEditForm, ProfileEditForm
from .models import Profile, Contact
from actions.models import Action
from actions.utils import create_action

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
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
                     .prefetch_related('target')[:10]
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})

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
            create_action(new_user, 'has created an account')
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
    
@login_required
def user_list(request):
    '''Vista que retorna todos los usuarios activos'''
    users = User.objects.filter(is_active=True)
    return render(
        request,
        'account/user/list.html',
        {
            'section': 'people',
            'users': users
        }
    )
    
@login_required
def user_datail(request, username):
    '''Vista que retorna un usuario en base al username'''
    user = get_object_or_404(
                User,
                username=username,
                is_active=True
            )
    
    return render(
        request,
        'account/user/detail.html',
        {
            'section': 'people',
            'user': user
        }
    )
    
@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
                
            return JsonResponse({'status': 'ok'})
            
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    
    return JsonResponse({'status': 'error'})