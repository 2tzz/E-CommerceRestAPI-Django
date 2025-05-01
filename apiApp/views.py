from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem, Product, Category
from .serializers import CartSerializer, ProductListSerializer , ProductDetailSerializer , CategoryListSerializer , CategoryDetailSerializer 

# Create your views here.


@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductListSerializer(products,many=True)
    return Response(serializer.data)



@api_view(['GET'])
def product_detail(request , slug) :
    prodct = Product.objects.get(slug=slug)
    serializer = ProductDetailSerializer(prodct)
    return Response(serializer.data)



@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories , many=True)
    return Response(serializer.data)



@api_view(['GET'])
def category_detail(request , slug):
    categories = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerializer(categories)
    return Response(serializer.data)


@api_view(['POST'])
def add_to_cart(request):
    cart_code = request.data.get('cart_code')
    product_id = request.data.get('product_id')

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)
    cartitem.quantity = 1
    cartitem.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data)

