import sys
import os

# Ensure the workspace directory is in the python path
sys.path.append(os.getcwd())

import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

def update_db():
    print("=== Deleting 'Rahul Sharma' profiles from Database ===")
    
    # Delete users containing 'rahul' in username, email, or first_name
    deleted_count = 0
    
    # 1. Filter by username start
    users = User.objects.filter(username__startswith='rahul') | User.objects.filter(email='rahul@gmail.com') | User.objects.filter(first_name__icontains='Rahul')
    
    for u in users:
        print(f"Deleting user: {u.username} ({u.email})")
        u.delete()
        deleted_count += 1

    print(f"=== Deleted {deleted_count} Rahul Sharma profiles. Clean up completed. ===")

if __name__ == '__main__':
    update_db()
