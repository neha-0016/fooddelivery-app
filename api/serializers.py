from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer, Restaurant, Food, Cart, CartItem, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email', 'phone', 'address', 'city', 'created_at']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.user:
            ret['full_name'] = f"{instance.user.first_name} {instance.user.last_name}".strip() or instance.user.username
            ret['email'] = instance.user.email
        else:
            ret['full_name'] = ""
            ret['email'] = ""
        return ret

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', '')
        email = validated_data.pop('email', '')

        # Generate unique username
        username = email.split('@')[0] if email else "user"
        if not username:
            username = "user"
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        first_name = ""
        last_name = ""
        if full_name:
            parts = full_name.split(' ', 1)
            first_name = parts[0]
            if len(parts) > 1:
                last_name = parts[1]

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    def update(self, instance, validated_data):
        full_name = validated_data.pop('full_name', None)
        email = validated_data.pop('email', None)

        user = instance.user
        if user:
            if email is not None:
                user.email = email
            if full_name is not None:
                parts = full_name.split(' ', 1)
                user.first_name = parts[0]
                user.last_name = parts[1] if len(parts) > 1 else ""
            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(write_only=True, required=False)
    food_name = serializers.CharField(write_only=True, required=False)
    availability = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Food
        fields = [
            'id', 'restaurant', 'name', 'description', 'category', 'price', 
            'is_available', 'created_at', 'restaurant_name', 'food_name', 'availability', 'image_url'
        ]
        extra_kwargs = {
            'restaurant': {'required': False},
            'name': {'required': False},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['restaurant_name'] = instance.restaurant.name if instance.restaurant else ""
        ret['availability'] = "Available" if instance.is_available else "Unavailable"
        ret['food_name'] = instance.name
        return ret

    def create(self, validated_data):
        restaurant_name = validated_data.pop('restaurant_name', None)
        food_name = validated_data.pop('food_name', None)
        availability = validated_data.pop('availability', None)

        if restaurant_name:
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_name,
                defaults={'address': 'Address to be updated', 'phone': '000-000-0000'}
            )
            validated_data['restaurant'] = restaurant

        if food_name:
            validated_data['name'] = food_name

        if availability is not None:
            validated_data['is_available'] = (availability.strip().lower() == 'available')

        return super().create(validated_data)

    def update(self, instance, validated_data):
        restaurant_name = validated_data.pop('restaurant_name', None)
        food_name = validated_data.pop('food_name', None)
        availability = validated_data.pop('availability', None)

        if restaurant_name:
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_name,
                defaults={'address': 'Address to be updated', 'phone': '000-000-0000'}
            )
            validated_data['restaurant'] = restaurant

        if food_name:
            validated_data['name'] = food_name

        if availability is not None:
            validated_data['is_available'] = (availability.strip().lower() == 'available')

        return super().update(instance, validated_data)

class CartItemSerializer(serializers.ModelSerializer):
    food_detail = FoodSerializer(source='food', read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'food', 'food_detail', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    customer_detail = CustomerSerializer(source='customer', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'customer_detail', 'items', 'created_at']

class OrderItemSerializer(serializers.ModelSerializer):
    food_detail = FoodSerializer(source='food', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'food', 'food_detail', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.user.username')
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_name', 'restaurant', 'restaurant_name',
            'status', 'total_price', 'delivery_address', 'items', 'created_at', 'updated_at'
        ]
