from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.TextField(null=True)
    pin_no = models.IntegerField(null=True)
    state = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username
            

class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class PostProduct(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    product_name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    category =models.ForeignKey(Category, on_delete=CASCADE)
    price=models.IntegerField(null=True)
    time_to_publish=models.DateTimeField()
    image=models.ImageField(upload_to='images')

    def __str__(self):
       return self.product_name
