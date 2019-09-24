from rest_framework import serializers
# from rest_framework import Shop
from .models import Shop, Product, Customer


class shopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
