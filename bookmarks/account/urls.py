from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # path(
    #     'login/',
    #     user_login,
    #     name='login'
    # ),
    # path(
    #     'login/',
    #     auth_views.LoginView.as_view(), 
    #     name='login',    
    # ),
    # path(
    #     'logout/',
    #     auth_views.LogoutView.as_view(),
    #     name='logout'
    # ),

    # # Sistema de cambio de password
    # path(
    #     'password-change/',
    #     auth_views.PasswordChangeView.as_view(),
    #     name='password_change'
    # ),

    # path(
    #     'password-change/done',
    #     auth_views.PasswordChangeDoneView.as_view(),
    #     name='password_change_done'
    # ),

    # # Sistema de reseteo de password
    # path(
    #     'password-reset/',
    #     auth_views.PasswordResetView.as_view(),
    #     name='password_reset'
    # ),

    # path(
    #     'password-reset/done/',
    #     auth_views.PasswordResetDoneView.as_view(),
    #     name='password_reset_done'
    # ),

    # path(
    #     'password-reset/<uidb64>/<token>/',
    #     auth_views.PasswordResetConfirmView.as_view(),
    #     name='password_reset_confirm'
    # ),

    # path(
    #     'password-reset/complete/',
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name='password_reset_complete'
    # ),
    
    # Urls para la autenticacion
    path('', include('django.contrib.auth.urls')),
    
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('users/', user_list, name='user_list'),
    path('users/follow/', user_follow, name='user_follow'),
    path('users/<username>', user_datail, name='user_detail'),
]
