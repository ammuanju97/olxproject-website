from django.contrib import admin
from .models import UserAddress, PostProduct, Category
# Register your models here.
admin.site.register(UserAddress)
admin.site.register(PostProduct)
admin.site.register(Category)