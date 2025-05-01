from rest_framework import serializers
from .models import CartItem, Product , Category , Cart

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'name' , 'slug' , 'description' , 'image' , 'price']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'name' ,  'slug' ,'image' ]


class CategoryListSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()
    class Meta :
        model= CartItem
        fields = ['id' , 'product' , 'quantity' , 'sub_total']

    def get_sub_total(self , cartitem):
        total = cartitem.product.price * cartitem.quantity
        return total
    
class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(read_only=True ,many=True)
    cart_total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id' , 'cart_code' , 'cartitems'  , 'cart_total']

    def get_cart_total(self , cart):
        items = cart.cartitems.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total








