from django.contrib.auth import views as auth_views
from django.conf import settings
from django.urls import path, include
from django.views.generic.base import TemplateView
from .forms import LoginForm
from . import views 
from .views import SignUp, LoginPage, user_logout, HomeView



urlpatterns = [
    path('', HomeView.as_view(), name = 'homeview'),
    path('aboutus/', views.aboutus, name = 'aboutus'),
    path('signup/', SignUp.as_view(), name = 'signup'),
    path('account-verify/<slug:token>', views.account_verify, name = 'account-verify'), 
    
    path('loginpage/', LoginPage.as_view(), name = 'loginpage'),
    path('user-logout/', views.user_logout, name = 'userlogout'),
    path("accounts/", include("django.contrib.auth.urls")),

    path('change-password/', auth_views.PasswordChangeView.as_view
    (template_name = 'registration/change-password.html', success_url = '/userhome'),
    name = 'change-password'),

    path('password-reset/', auth_views.PasswordResetView.as_view
    (template_name = 'registration/password_reset_form.html',
    ),name = 'password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name = 'registration/password_reset_done.html'),
        name = 'password_reset_done' ),

    path('password-reset-confirm/<uidb64>/token/',
        auth_views.PasswordResetConfirmView.as_view(
        template_name = 'registration/password_reset_confirm.html'),
        name = 'password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'registration/password_reset_complete.html'),
        name = 'password_reset_complete'),

    path('cart/', views.cart, name = 'cart'),
    path('allproducts/', views.allproducts, name = 'allproducts'),
    path('popularitem/', views.popularitem, name = 'popularitem'),
    path('newarrival/', views.newarrival, name = 'newarrival'),
]
