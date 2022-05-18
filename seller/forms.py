from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.forms import fields
from home.models import Useradd
from .models import UserAddress, PostProduct, Category

# from .models import

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields=('first_name', 'last_name', 'email', 'username')


class AddressDetForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields=('address','pin_no','state','city')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Useradd
        fields=('mobile_no',)


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = PostProduct
        fields=('product_name','description','category','price','time_to_publish','image')