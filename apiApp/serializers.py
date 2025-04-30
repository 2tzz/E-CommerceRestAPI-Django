from rest_framework import serializers
from .models import Product , Category

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'name' , 'slug' , 'description' , 'image' , 'price']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'name' ,'description' ,  'slug' , 'description' , 'image' , 'price']


class CategorySerializer(serializers.ModelSerializer):
    prodacts = ProductListSerializer(many=True , read_only=True)
    class Meta:
        model = Category
        fields = ['id' , 'name' , 'image' , 'products']

