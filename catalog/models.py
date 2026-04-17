from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='children'
    )

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_main_image(self):
        main = self.images.filter(is_main=True).first()
        if main:
            return main
        return self.images.first()

    def get_discounted_price(self):
        today = timezone.now().date()
        discount = self.discounts.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        ).order_by('-discount_percent').first()
        if discount:
            factor = (100 - discount.discount_percent) / 100
            return round(self.price * factor, 2)
        return self.price

    def get_discount_percent(self):
        today = timezone.now().date()
        discount = self.discounts.filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        ).order_by('-discount_percent').first()
        if discount:
            return discount.discount_percent
        return None


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f'Image for {self.product.name}'


class Characteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}: {self.value}'


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    discount_percent = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.discount_percent}% off {self.product.name}'
