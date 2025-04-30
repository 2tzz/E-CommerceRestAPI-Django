from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductListSerializer

# Create your views here.


@api_view(['GET'])
def product_list(request):
    products = Product.objects.filter(featured=True)
    serializer = ProductListSerializer(products,many=True)
    return Response(serializer.data)



@api_view(['GET'])
def product_detail(request , slug) :