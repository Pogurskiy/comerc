from django.contrib import admin
from .models import Category, Product, ProductImage, Characteristic, Discount


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class CharacteristicInline(admin.TabularInline):
    model = Characteristic
    extra = 1


class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available', 'views_count', 'created')
    list_filter = ('is_available', 'category')
    list_editable = ('price', 'stock', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, CharacteristicInline, DiscountInline]
    readonly_fields = ('views_count', 'created', 'updated')
