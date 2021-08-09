from customer.models import PostProduct
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db import models

# Create your models here.
class BuyProduct(models.Model):
    seller_name = models.ForeignKey(User, on_delete = CASCADE, related_name = 'sellername')
    buyer_name = models.ForeignKey(User, on_delete = CASCADE, related_name = 'buyername')
    product_name = models.ForeignKey(PostProduct, on_delete = CASCADE)
    buy_status = models.BooleanField(default = False)
    buyer_price = models.IntegerField()

    def __str__(self):
        return self.buyer_name.username
