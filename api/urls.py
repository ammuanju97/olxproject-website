from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . views import ProductList, UserRegistration, LoginAPI
from knox import views as knox_views

urlpatterns = [
    path('product-list/', ProductList.as_view(), name = 'productlist'),
    path('user-registration/', UserRegistration.as_view(), name = 'userregister'),
    path('login/', LoginAPI.as_view(), name='api-login'),

]