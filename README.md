# 🚀 Enjoy Eats - Premium Food Delivery Web Application

Welcome to **Enjoy Eats**, a modern, responsive full-stack food delivery web application built using Django, Django REST Framework (DRF), and SQLite, styled with a premium vanilla CSS light-mode theme.

---

## 📸 Screenshots & Visual Demonstrations

Here is a neatly arranged overview of the application's user interface, database tables, and API testing logs.

### 🔐 1. Customer Portal Login UI
This screenshot showcases the clean, light-themed login portal featuring quick account selectors for registered customer profiles like **NEHA**.

![Login Page UI](docs/images/login_page.png)

---

### 📂 2. Database Schema (SQLite)

#### 🍔 Food Catalogue Table (`api_food`)
A snapshot of the seeded menu items database, displaying various main course biryanis, fresh juices, pizzas, and desserts along with pricing details.

![SQLite Food Table](docs/images/db_foods.png)

#### 🔑 Auth Permissions Table (`auth_permission`)
A snapshot of the internal Django authentication permission schema configuration.

![SQLite Permissions Table](docs/images/db_permissions.png)

---

### 📡 3. REST API Endpoints Testing

#### 👤 POST /api/customers/add/
Demonstration of adding a customer using a JSON payload via an HTTP client, returning `201 Created` with default user profile values.

![POST Customer API Response](docs/images/post_customer_api.png)

#### 🏪 GET /api/restaurants/
Testing the restaurant retrieval endpoint returning `200 OK` with restaurant details and banner image URLs.

![GET Restaurants API Response](docs/images/get_restaurants_api.png)
