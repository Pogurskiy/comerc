# Comerc — Django E-Commerce Store

A full-featured online store built with Python + Django, Bootstrap 5, and Django REST Framework.

## Features

- **User Auth**: Registration & login via email + password (custom User model)
- **Personal Cabinet**: Profile editing + order history
- **Product Catalog**: Categories, filters, search, sorting (price / popularity / newest)
- **Product Detail**: Photo gallery, description, characteristics table, price with discount badge
- **Shopping Cart**: Session-based; add / remove / update quantity
- **Checkout**: Delivery form, simulated payment, Order + OrderItem creation
- **Recommendations**: Recently-viewed and same-category recommended products
- **SEO-friendly URLs**: slug-based for categories and products
- **Django Messages**: Success / error notifications (Bootstrap alerts)
- **Admin Panel**: Full CRUD for Products, Categories, Characteristics, Discounts, Gallery, Orders
- **REST API** (DRF): Endpoints for catalogue, cart, checkout, profile, orders

## Quick Start

```bash
# 1. Clone & create virtual environment
git clone https://github.com/Pogurskiy/comerc.git
cd comerc
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Load seed data  (creates admin + 5 categories + 22 products + discounts)
python manage.py seed

# 5. Run development server
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser.

### Admin access

| URL | Credentials |
|-----|-------------|
| <http://127.0.0.1:8000/admin/> | `admin@shop.com` / `admin123` |

## Project Structure

```
comerc/          Django project settings
accounts/        Custom User, registration, login, profile
catalog/         Category & Product models, views, admin
cart/            Session-based Cart + views
orders/          Order / OrderItem models, checkout flow
api/             Django REST Framework endpoints
templates/       Jinja2-compatible Django templates (Bootstrap 5)
static/          CSS & JS
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/categories/` | List all categories |
| GET | `/api/products/` | List products (filter: `?category=<slug>&q=<query>&sort=price\|-price\|views\|newest`) |
| GET | `/api/products/<id>/` | Product detail |
| GET/POST | `/api/cart/` | View cart / add item |
| POST | `/api/cart/remove/` | Remove item |
| POST | `/api/checkout/` | Create order |
| GET/PUT | `/api/profile/` | View/update profile |
| GET | `/api/orders/` | List user orders |

## Tech Stack

- **Backend**: Python 3.10+, Django 4.2, Django REST Framework
- **Frontend**: Bootstrap 5 (CDN), custom CSS / JS
- **DB**: SQLite (dev); swap to PostgreSQL via `DATABASE_URL`
- **Images**: Pillow; placeholder images shown when no upload
