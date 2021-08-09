from django.contrib.auth import models
from django.db.models import fields
from django import forms
from .models import BuyProduct

class BuyerForm(forms.ModelForm):
    class Meta:
        model = BuyProduct
        exclude = ['seller_name', 'buyer_name', 'product_name', 'buy_status']
        fields = ('buyer_price',)
