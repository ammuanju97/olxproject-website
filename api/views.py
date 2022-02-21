from customer.models import PostProduct
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, UserRegister
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from django.contrib.auth import login


# Create your views here.
class ProductList(APIView):
    def get(self, request):
        product = PostProduct.objects.all()
        serializer = ProductSerializer(product, many = True)
        return Response(serializer.data)


class UserRegistration(APIView):
    def post(self, request, format = None):
        serializer = UserRegister(data = request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'user registered sucessfully'
            data['username'] = account.username
            data['email'] = account.email
            token, create = Token.objects.get_or_create(user = account)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)


class LoginAPI(KnoxLoginView):
    """
    LoginApi
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
