from django.contrib import admin
from .models import Customer, Restaurant, Food, Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price'] # Price is frozen at checkout and shouldn't be edited easily

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'city', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'city']
    list_filter = ['created_at']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'phone']

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'restaurant', 'price', 'is_available', 'created_at']
    list_filter = ['is_available', 'restaurant']
    search_fields = ['name']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_at']
    inlines = [CartItemInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'restaurant', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'restaurant', 'created_at']
    search_fields = ['id', 'customer__user__username', 'restaurant__name']
    inlines = [OrderItemInline]
