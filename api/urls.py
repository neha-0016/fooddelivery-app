from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CustomerViewSet, RestaurantViewSet, FoodViewSet,
    CartViewSet, CartItemViewSet, OrderViewSet, OrderItemViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'foods', FoodViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    # Custom Customer URL mappings
    path('customers/add/', CustomerViewSet.as_view({'post': 'create'}), name='customer-add'),
    path('customers/update/<int:pk>/', CustomerViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='customer-update'),
    path('customers/delete/<int:pk>/', CustomerViewSet.as_view({'delete': 'destroy'}), name='customer-delete'),

    # Custom Restaurant URL mappings
    path('restaurants/add/', RestaurantViewSet.as_view({'post': 'create'}), name='restaurant-add'),
    path('restaurants/update/<int:pk>/', RestaurantViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='restaurant-update'),
    path('restaurants/delete/<int:pk>/', RestaurantViewSet.as_view({'delete': 'destroy'}), name='restaurant-delete'),
    path('restaurants/search/', RestaurantViewSet.as_view({'get': 'search'}), name='restaurant-search'),

    # Custom Food URL mappings
    path('foods/add/', FoodViewSet.as_view({'post': 'create'}), name='food-add'),
    path('foods/update/<int:pk>/', FoodViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='food-update'),
    path('foods/delete/<int:pk>/', FoodViewSet.as_view({'delete': 'destroy'}), name='food-delete'),
    path('foods/search/', FoodViewSet.as_view({'get': 'search'}), name='food-search'),

    # Custom Order URL mappings
    path('orders/add/', OrderViewSet.as_view({'post': 'create'}), name='order-add'),
    path('orders/update/<int:pk>/', OrderViewSet.as_view({'put': 'update', 'patch': 'partial_update'}), name='order-update'),
    path('orders/delete/<int:pk>/', OrderViewSet.as_view({'delete': 'destroy'}), name='order-delete'),

    path('', include(router.urls)),
]
