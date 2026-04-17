from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from catalog.models import Category, Product
from orders.models import Order, OrderItem
from cart.cart import Cart
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    OrderSerializer, ProfileSerializer,
)


class CategoryListAPI(APIView):
    def get(self, request):
        cats = Category.objects.all()
        return Response(CategorySerializer(cats, many=True).data)


class ProductListAPI(APIView):
    def get(self, request):
        products = Product.objects.filter(is_available=True)
        category_slug = request.query_params.get('category')
        q = request.query_params.get('q')
        if category_slug:
            products = products.filter(category__slug=category_slug)
        if q:
            from django.db.models import Q
            products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductDetailAPI(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_available=True)
        except Product.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProductDetailSerializer(product, context={'request': request}).data)


class CartAPI(APIView):
    def get(self, request):
        cart = Cart(request)
        items = []
        for item in cart:
            items.append({
                'product_id': item['product'].id,
                'product_name': item['product'].name,
                'price': str(item['price']),
                'quantity': item['quantity'],
                'total_price': str(item['total_price']),
            })
        return Response({'items': items, 'total': str(cart.get_total_price())})


class CartAddAPI(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        try:
            product = Product.objects.get(pk=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        cart = Cart(request)
        cart.add(product, quantity=quantity)
        return Response({'message': 'Added', 'cart_count': len(cart)})


class CartRemoveAPI(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        cart = Cart(request)
        cart.remove(product)
        return Response({'message': 'Removed', 'cart_count': len(cart)})


class CheckoutAPI(APIView):
    def post(self, request):
        cart = Cart(request)
        if len(cart) == 0:
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        required = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code']
        for field in required:
            if not request.data.get(field):
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email'],
            phone=request.data['phone'],
            address=request.data['address'],
            city=request.data['city'],
            postal_code=request.data['postal_code'],
            payment_method=request.data.get('payment_method', 'card'),
            notes=request.data.get('notes', ''),
            total_price=cart.get_total_price(),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product'].name,
                price=item['price'],
                quantity=item['quantity'],
            )
        cart.clear()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class ProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data)
