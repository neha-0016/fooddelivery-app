from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import transaction
from .models import Customer, Restaurant, Food, Cart, CartItem, Order, OrderItem
from .serializers import (
    UserSerializer, CustomerSerializer, RestaurantSerializer, FoodSerializer,
    CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            restaurants = Restaurant.objects.filter(name__icontains=query)
        else:
            restaurants = Restaurant.objects.all()
        serializer = self.get_serializer(restaurants, many=True)
        return Response(serializer.data)

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_queryset(self):
        queryset = Food.objects.all()
        restaurant_id = self.request.query_params.get('restaurant')
        if restaurant_id is not None:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            foods = Food.objects.filter(name__icontains=query)
        else:
            foods = Food.objects.all()
        serializer = self.get_serializer(foods, many=True)
        return Response(serializer.data)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        food_id = request.data.get('food_id')
        quantity = int(request.data.get('quantity', 1))

        if not food_id:
            return Response({'error': 'food_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            food = Food.objects.get(id=food_id)
        except Food.DoesNotExist:
            return Response({'error': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)

        if not food.is_available:
            return Response({'error': 'Food item is not available'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, food=food)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        food_id = request.data.get('food_id')
        
        if not food_id:
            return Response({'error': 'food_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = CartItem.objects.get(cart=cart, food_id=food_id)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # Check if direct single-item order payload is sent
        customer_name = request.data.get('customer_name')
        food_name = request.data.get('food_name')

        if customer_name and food_name:
            quantity = int(request.data.get('quantity', 1))
            price_val = float(request.data.get('price', 0.00))

            from django.db.models import Q
            parts = customer_name.split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

            # Try to query Customer
            customers = Customer.objects.filter(
                Q(user__first_name=first_name, user__last_name=last_name) |
                Q(user__username=customer_name)
            )
            if not customers.exists():
                # Automatically create Customer
                username = customer_name.replace(' ', '_').lower()
                user, created = User.objects.get_or_create(username=username, defaults={'first_name': first_name, 'last_name': last_name})
                customer, created = Customer.objects.get_or_create(user=user, defaults={'phone': '0000000000', 'address': 'KPHB Colony', 'city': 'Hyderabad'})
            else:
                customer = customers.first()

            # Resolve Food
            food = Food.objects.filter(name=food_name).first()
            if not food:
                # Create a default restaurant and food item if it doesn't exist
                restaurant, created = Restaurant.objects.get_or_create(
                    name="Spicy Kitchen",
                    defaults={'address': 'Hyderabad', 'phone': '000-000-0000'}
                )
                food = Food.objects.create(
                    restaurant=restaurant,
                    name=food_name,
                    price=price_val,
                    is_available=True,
                    category="Main Course"
                )

            restaurant = food.restaurant
            total_price = quantity * price_val
            delivery_address = customer.address or "KPHB Colony"

            with transaction.atomic():
                order = Order.objects.create(
                    customer=customer,
                    restaurant=restaurant,
                    delivery_address=delivery_address,
                    status='Pending',
                    total_price=total_price
                )
                OrderItem.objects.create(
                    order=order,
                    food=food,
                    quantity=quantity,
                    price=price_val
                )

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Fallback to Cart Checkout
        customer_id = request.data.get('customer')
        restaurant_id = request.data.get('restaurant')
        delivery_address = request.data.get('delivery_address')

        if not all([customer_id, restaurant_id, delivery_address]):
            return Response(
                {'error': 'customer, restaurant, and delivery_address are all required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            customer = Customer.objects.get(id=customer_id)
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except (Customer.DoesNotExist, Restaurant.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)

        # Get customer's cart
        try:
            cart = Cart.objects.get(customer=customer)
        except Cart.DoesNotExist:
            return Response({'error': 'Customer has no active cart'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if restaurant matches items in cart
        for item in cart_items:
            if item.food.restaurant != restaurant:
                return Response(
                    {'error': f"Food item '{item.food.name}' belongs to a different restaurant ({item.food.restaurant.name})"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Create the Order and its items within a database transaction
        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                restaurant=restaurant,
                delivery_address=delivery_address,
                status='Pending',
                total_price=0
            )

            total = 0
            for item in cart_items:
                price = item.food.price
                quantity = item.quantity
                OrderItem.objects.create(
                    order=order,
                    food=item.food,
                    quantity=quantity,
                    price=price
                )
                total += price * quantity

            order.total_price = total
            order.save()

            # Clear the cart items after successfully creating the order
            cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
