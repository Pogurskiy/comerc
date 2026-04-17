from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

User = get_user_model()


CATEGORIES = [
    ('Electronics', 'electronics', 'Gadgets, devices and accessories'),
    ('Clothing', 'clothing', 'Fashion for everyone'),
    ('Books', 'books', 'Knowledge and entertainment'),
    ('Sports', 'sports', 'Equipment and apparel for every sport'),
    ('Home & Garden', 'home-garden', 'Everything for your home and garden'),
]

PRODUCTS = [
    # Electronics
    ('Wireless Headphones Pro', 'electronics', 149.99, 50, 'Premium noise-cancelling wireless headphones with 30-hour battery life and rich sound.'),
    ('Smart Watch Ultra', 'electronics', 299.99, 30, 'Feature-packed smartwatch with health tracking, GPS, and 7-day battery life.'),
    ('USB-C Hub 7-in-1', 'electronics', 39.99, 100, 'Expand your laptop connectivity with 4K HDMI, USB 3.0, SD card reader, and more.'),
    ('Mechanical Keyboard RGB', 'electronics', 89.99, 40, 'Tactile mechanical keyboard with customizable RGB backlighting, perfect for gaming and typing.'),
    ('Portable Bluetooth Speaker', 'electronics', 59.99, 60, 'Waterproof portable speaker with 360° sound and 12-hour playtime.'),
    # Clothing
    ('Classic Denim Jacket', 'clothing', 79.99, 80, 'Timeless denim jacket, perfect for layering in any season.'),
    ('Running Shoes Air Max', 'clothing', 119.99, 45, 'Lightweight and cushioned running shoes for maximum performance.'),
    ('Merino Wool Sweater', 'clothing', 69.99, 55, 'Soft and warm merino wool sweater, ideal for cool days.'),
    ('Slim Fit Chinos', 'clothing', 49.99, 70, 'Versatile slim-fit chinos that go from office to weekend effortlessly.'),
    # Books
    ('Clean Code by Robert Martin', 'books', 34.99, 200, 'A handbook of agile software craftsmanship. Essential reading for every developer.'),
    ('The Pragmatic Programmer', 'books', 32.99, 180, 'Your journey to mastery. Timeless advice for modern software engineers.'),
    ('Django for Beginners', 'books', 24.99, 150, 'Build websites with Python and Django from scratch.'),
    ('Python Crash Course', 'books', 29.99, 160, 'A hands-on, project-based introduction to programming in Python.'),
    # Sports
    ('Yoga Mat Premium', 'sports', 44.99, 90, 'Extra thick, non-slip yoga mat for comfort and stability in every pose.'),
    ('Resistance Bands Set', 'sports', 24.99, 120, 'Set of 5 resistance bands for full-body workouts anywhere.'),
    ('Water Bottle Insulated', 'sports', 19.99, 200, 'Keep drinks cold for 24 hours or hot for 12 hours with this stainless steel bottle.'),
    ('Jump Rope Speed', 'sports', 14.99, 150, 'Adjustable speed jump rope for cardio training and fitness goals.'),
    # Home & Garden
    ('Indoor Plant Pot Set', 'home-garden', 34.99, 80, 'Set of 3 decorative ceramic pots perfect for succulents and small plants.'),
    ('Smart LED Bulb Pack', 'home-garden', 29.99, 100, 'Pack of 4 color-changing smart bulbs, controlled via app or voice assistant.'),
    ('Coffee Pour-Over Set', 'home-garden', 39.99, 60, 'Artisan coffee brewing set with glass carafe, filter holder and 50 filters.'),
    ('Aromatherapy Diffuser', 'home-garden', 27.99, 75, 'Ultrasonic essential oil diffuser with LED mood light and auto shut-off.'),
    ('Garden Tool Kit', 'home-garden', 49.99, 40, 'Complete 10-piece garden tool set with ergonomic handles and storage bag.'),
]

CHARACTERISTICS = {
    'Wireless Headphones Pro': [
        ('Battery Life', '30 hours'), ('Connectivity', 'Bluetooth 5.2'),
        ('Driver Size', '40mm'), ('Weight', '250g'),
    ],
    'Smart Watch Ultra': [
        ('Display', '1.4" AMOLED'), ('Battery', '7 days'),
        ('Water Resistance', '5ATM'), ('Sensors', 'HR, SpO2, GPS'),
    ],
    'Running Shoes Air Max': [
        ('Upper Material', 'Mesh'), ('Sole', 'Rubber'),
        ('Drop', '10mm'), ('Weight', '280g'),
    ],
    'Yoga Mat Premium': [
        ('Thickness', '6mm'), ('Material', 'TPE'),
        ('Size', '183 x 61 cm'), ('Weight', '1.1kg'),
    ],
}


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Creating admin user...')
        if not User.objects.filter(email='admin@shop.com').exists():
            User.objects.create_superuser(
                email='admin@shop.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
            )
            self.stdout.write(self.style.SUCCESS('Admin created: admin@shop.com / admin123'))
        else:
            self.stdout.write('Admin already exists.')

        from catalog.models import Category, Product, Characteristic, Discount

        self.stdout.write('Creating categories...')
        cat_map = {}
        for name, slug, description in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': description}
            )
            cat_map[slug] = cat

        self.stdout.write('Creating products...')
        today = timezone.now().date()
        for i, (name, cat_slug, price, stock, description) in enumerate(PRODUCTS):
            slug = slugify(name)
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'category': cat_map[cat_slug],
                    'price': Decimal(str(price)),
                    'stock': stock,
                    'description': description,
                    'is_available': True,
                    'views_count': i * 7,
                }
            )
            if created:
                chars = CHARACTERISTICS.get(name, [])
                for char_name, char_value in chars:
                    Characteristic.objects.get_or_create(
                        product=product, name=char_name,
                        defaults={'value': char_value}
                    )
                if i % 3 == 0:
                    Discount.objects.get_or_create(
                        product=product,
                        defaults={
                            'discount_percent': 10 + (i % 20),
                            'start_date': today - timedelta(days=7),
                            'end_date': today + timedelta(days=30),
                            'is_active': True,
                        }
                    )

        self.stdout.write(self.style.SUCCESS(
            f'Seed complete. Categories: {Category.objects.count()}, '
            f'Products: {Product.objects.count()}'
        ))
