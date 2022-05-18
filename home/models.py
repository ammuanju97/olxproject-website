from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class userreg(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    token = models.CharField(max_length = 150)
    verify = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username


class Useradd(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    mobile_no = models.CharField(max_length = 10)
    
    def __str__(self):
          return  self.user.username
