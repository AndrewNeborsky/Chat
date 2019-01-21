from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='', verbose_name='Image', null=True)
    age = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True)
    site = models.CharField(max_length=255, blank=True)
