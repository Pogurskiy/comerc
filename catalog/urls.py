from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('catalog/<slug:slug>/', views.product_detail, name='product_detail'),
]
