from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Cart, CartItem, Product, Category , Review, Wishlist
from .serializers import WishListSerializer , ReviewSerializer, CartSerializer, ProductListSerializer , ProductDetailSerializer , CategoryListSerializer , CategoryDetailSerializer , CartItemSerializer

# Create your views here.

User = get_user_model()


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

@api_view(['PUT'])
def update_cartitem_quantity(request):
    # Get parameters from query params (for PUT with URL parameters)
    cartitem_id = request.query_params.get('item_id')
    quantity = request.query_params.get('quantity')
    
    # Alternatively, if you want to use request.data (for PUT with form/json body):
    # cartitem_id = request.data.get('item_id')
    # quantity = request.data.get('quantity')

    if not cartitem_id or not quantity:
        return Response({'error': 'Both item_id and quantity are required.'}, status=400)

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return Response({'error': 'Quantity must be a valid integer.'}, status=400)

    try:
        cartitem = CartItem.objects.get(id=cartitem_id)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found.'}, status=404)

    cartitem.quantity = quantity
    cartitem.save()

    serializer = CartItemSerializer(cartitem)
    return Response({'data': serializer.data, 'message': 'Cartitem updated successfully!'})



@api_view(['POST'])
def add_review(request):
    product_id = request.data.get('product_id')
    email = request.data.get('email')
    rating = request.data.get('rating')
    review_text = request.data.get('review')

    try:
        product = Product.objects.get(id=product_id)
        user = User.objects.get(email=email)
    except (Product.DoesNotExist, User.DoesNotExist) as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

    if Review.objects.filter(product=product, user=user).exists():
        return Response({'error': 'You have already reviewed this product.'}, status=status.HTTP_400_BAD_REQUEST)

    review = Review.objects.create(
        product=product,
        user=user,
        rating=rating,
        review=review_text
    )
    
    serializer = ReviewSerializer(review)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['PUT'])
def update_review(request, pk):
    try:
        review = Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Check both request.data (for form/json body) and query_params (for URL params)
    rating = request.data.get('rating') or request.query_params.get('rating')
    review_text = request.data.get('review') or request.query_params.get('review')

    if not rating:
        return Response({'error': 'Rating is required.'}, status=status.HTTP_400_BAD_REQUEST)

    review.rating = rating
    if review_text:  # review text is optional for update
        review.review = review_text
    review.save()

    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_review(request , pk):
    review = Review.objects.get(id=pk)
    review.delete()


    return Response("Review Deleted Sucessfully" , status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_to_wishlist(request):
    email = request.beta.get('email')
    product_id = request.data.get('product_id')


    user = User.objects.get(email=email)
    product = Product.objects.get(id=product_id)

    wishlist = Wishlist.objects.filter(user = user , product = product)
    if wishlist:
        wishlist.delete()
        return Response('wishlist deleted sucessfully!' , status=204)

    new_wishlist = Wishlist.objects.filter(user=user , product=product)
    serializer = WishListSerializer(new_wishlist)
    return Response(serializer.data)
