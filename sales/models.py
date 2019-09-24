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
    sale_per = models.CharField(max_length=200, default='')
    branded = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=200, default='')
    password2 = models.CharField(max_length=200, default='')


class Product(models.Model):
    Shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='test.jpg', null=True, upload_to='shop')
    product_name = models.CharField(max_length=200, default='')
    price = models.CharField(max_length=200, default='')
    discount = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default='')

class Employee(models.Model):
    eid = models.CharField(max_length=20)
    ename = models.CharField(max_length=100)
    eemail = models.EmailField()
    econtact = models.CharField(max_length=15)
    class Meta:
        db_table = "employee"