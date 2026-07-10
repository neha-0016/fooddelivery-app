import sys
import os

# Ensure the workspace directory is in the python path
sys.path.append(os.getcwd())

import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Customer, Restaurant, Food

def seed_data():
    print("=== Seeding Updated Restaurant and Food Data for NEHA ===")

    # 1. Update/Create NEHA Customer Profile
    # Remove Rahul if exists to avoid confusion
    User.objects.filter(username='rahul').delete()
    
    neha_user, created = User.objects.get_or_create(
        username='neha',
        defaults={
            'email': 'neha@gmail.com',
            'first_name': 'NEHA',
            'last_name': ''
        }
    )
    if created:
        neha_user.set_password('password123')
        neha_user.save()

    neha_customer, c_created = Customer.objects.get_or_create(
        user=neha_user,
        defaults={
            'phone': '9876543210',
            'address': 'KPHB Colony',
            'city': 'Hyderabad'
        }
    )
    print(f"Customer NEHA (Created: {c_created})")

    # 2. Add New Restaurants

    # Biryani Hub
    bh, created = Restaurant.objects.get_or_create(
        name='Biryani Hub',
        defaults={
            'description': 'The ultimate destination for biryani lovers.',
            'address': 'Madhapur Road #3, Hyderabad',
            'phone': '9876543204',
            'is_active': True,
            'image_url': 'https://images.unsplash.com/photo-1633945274405-b6c8069047b0?w=500'
        }
    )
    print(f"Restaurant: Biryani Hub (Created: {created})")

    bh_menu = [
        {"name": "Veg Biryani", "category": "Main Course", "price": 199.00, "description": "Fragrant basmati rice cooked with assorted fresh vegetables and spices.", "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500"},
        {"name": "Egg Biryani", "category": "Main Course", "price": 229.00, "description": "Spiced boiled eggs cooked with aromatic long grain basmati rice.", "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500"},
        {"name": "Chicken Kebab", "category": "Main Course", "price": 249.00, "description": "Crispy fried chicken bites marinated in hot Indian spices.", "image_url": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=500"}
    ]

    for item in bh_menu:
        food, f_created = Food.objects.get_or_create(
            restaurant=bh,
            name=item["name"],
            defaults={
                "category": item["category"],
                "price": item["price"],
                "description": item["description"],
                "is_available": True,
                "image_url": item["image_url"]
            }
        )
        print(f"  Food: {food.name} (Created: {f_created})")

    # Dessert Delights
    dd, created = Restaurant.objects.get_or_create(
        name='Dessert Delights',
        defaults={
            'description': 'Irresistible cakes, pastries, pudding, and sweet treats.',
            'address': 'Banjara Hills, Hyderabad',
            'phone': '9876543205',
            'is_active': True,
            'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500'
        }
    )
    print(f"Restaurant: Dessert Delights (Created: {created})")

    dd_menu = [
        {"name": "Chocolate Truffle Cake", "category": "Desserts", "price": 149.00, "description": "Rich and dense chocolate cake glazed with dark chocolate ganache.", "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500"},
        {"name": "Blueberry Cheesecake", "category": "Desserts", "price": 189.00, "description": "Creamy New York style cheesecake topped with sweet blueberry compote.", "image_url": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500"},
        {"name": "Mango Pudding", "category": "Desserts", "price": 99.00, "description": "Silky smooth mango flavored pudding made with fresh pulp.", "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500"}
    ]

    for item in dd_menu:
        food, f_created = Food.objects.get_or_create(
            restaurant=dd,
            name=item["name"],
            defaults={
                "category": item["category"],
                "price": item["price"],
                "description": item["description"],
                "is_available": True,
                "image_url": item["image_url"]
            }
        )
        print(f"  Food: {food.name} (Created: {f_created})")

    # Juice Junction
    jj, created = Restaurant.objects.get_or_create(
        name='Juice Junction',
        defaults={
            'description': 'Freshly squeezed fruit juices, shakes, and healthy detox drinks.',
            'address': 'Kondapur, Hyderabad',
            'phone': '9876543206',
            'is_active': True,
            'image_url': 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=500'
        }
    )
    print(f"Restaurant: Juice Junction (Created: {created})")

    jj_menu = [
        {"name": "Fresh Orange Juice", "category": "Juices", "price": 89.00, "description": "100% natural cold pressed orange juice, rich in Vitamin C.", "image_url": "https://images.unsplash.com/photo-1613478223719-2ab802602423?w=500"},
        {"name": "Watermelon Splash", "category": "Juices", "price": 79.00, "description": "Refreshing fresh watermelon juice served chilled.", "image_url": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=500"},
        {"name": "Mango Smoothie", "category": "Juices", "price": 129.00, "description": "Thick smoothie made with sweet mangoes, milk, and honey.", "image_url": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=500"},
        {"name": "Green Detox Juice", "category": "Juices", "price": 99.00, "description": "Healthy blend of cucumber, spinach, green apple, mint, and lemon.", "image_url": "https://images.unsplash.com/photo-1610970881699-44a5587caa90?w=500"}
    ]

    for item in jj_menu:
        food, f_created = Food.objects.get_or_create(
            restaurant=jj,
            name=item["name"],
            defaults={
                "category": item["category"],
                "price": item["price"],
                "description": item["description"],
                "is_available": True,
                "image_url": item["image_url"]
            }
        )
        print(f"  Food: {food.name} (Created: {f_created})")

    print("=== Database Seeded Successfully ===")

if __name__ == '__main__':
    seed_data()
