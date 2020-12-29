from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user_token = models.CharField(max_length=64)
    user_icon = models.ImageField(upload_to='icons', null=True) #static icons