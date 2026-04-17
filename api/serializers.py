from rest_framework import serializers
from catalog.models import Category, Product, ProductImage, Characteristic
from orders.models import Order, OrderItem
from accounts.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['name', 'value']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    discounted_price = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'discounted_price',
            'discount_percent', 'stock', 'is_available',
            'category_name', 'main_image',
        ]

    def get_discounted_price(self, obj):
        return str(obj.get_discounted_price())

    def get_discount_percent(self, obj):
        return obj.get_discount_percent()

    def get_main_image(self, obj):
        img = obj.get_main_image()
        if img and img.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(img.image.url)
        return None


class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    characteristics = CharacteristicSerializer(many=True, read_only=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ['description', 'images', 'characteristics', 'created']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'postal_code', 'status', 'payment_method',
            'is_paid', 'total_price', 'created', 'items',
        ]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address']
        read_only_fields = ['email']
