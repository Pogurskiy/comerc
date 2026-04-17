from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('categories/', views.CategoryListAPI.as_view(), name='categories'),
    path('products/', views.ProductListAPI.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailAPI.as_view(), name='product_detail'),
    path('cart/', views.CartAPI.as_view(), name='cart'),
    path('cart/add/', views.CartAddAPI.as_view(), name='cart_add'),
    path('cart/remove/', views.CartRemoveAPI.as_view(), name='cart_remove'),
    path('checkout/', views.CheckoutAPI.as_view(), name='checkout'),
    path('profile/', views.ProfileAPI.as_view(), name='profile'),
    path('orders/', views.OrderListAPI.as_view(), name='orders'),
]
