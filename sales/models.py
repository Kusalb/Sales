from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class CustomUser(AbstractUser):
    is_admin = models.BooleanField('Admin', default=False)
    is_shop = models.BooleanField('Shop', default=False)
    is_customer = models.BooleanField('Customer', default=False)


class Customer(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=100, default='')
    contact = models.CharField(max_length=20, default='')
    gender = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')
    password2 = models.CharField(max_length=200, default='')


class Shop(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    shop_name = models.CharField(max_length=200, default='')
    contact = models.CharField(max_length=200, default='')
    location = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=200, default='')
    contact_person = models.CharField(max_length=200, default='')
    branded = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')
    password2 = models.CharField(max_length=200, default='')


class Product(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='test.jpg', null=True, upload_to='shop')
    product_name = models.CharField(max_length=200, default='')
    price = models.CharField(max_length=200, default='')
    discount = models.CharField(max_length=200, default='')
    old_price = models.CharField(max_length=200, default='')
    is_approve = models.BooleanField(default=False)

class Deals(models.Model):
    CustomUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='test.jpg', null=True, upload_to='deal')
    deal_name = models.CharField(max_length=100)
    valid_from = models.DateField(max_length=100)
    valid_till = models.DateField(max_length=100)
    discount_per = models.CharField(max_length=100)
    is_approve = models.BooleanField(default=False)

class Advertisement(models.Model):
    image = models.ImageField(default='test.jpg', null=True, upload_to='advertisement')


