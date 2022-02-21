from  customer.models import PostProduct
from django.contrib.auth import get_user_model
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostProduct
        fields = '__all__'


User = get_user_model()
class UserRegister(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type' : 'password'}, write_only = True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "password2"]
    def save(self):
        reg = User(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'password does not match'})
        reg.set_password(password)
        reg.save()
        return reg
        