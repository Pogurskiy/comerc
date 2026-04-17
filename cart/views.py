from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from catalog.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk, is_available=True)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1
    update = request.POST.get('update', '') == 'true'
    cart.add(product, quantity=quantity, update_quantity=update)
    messages.success(request, f'"{product.name}" added to cart.')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    cart.remove(product)
    messages.info(request, 'Item removed from cart.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, pk=pk)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            cart.remove(product)
            messages.info(request, 'Item removed from cart.')
        else:
            cart.add(product, quantity=quantity, update_quantity=True)
            messages.success(request, 'Cart updated.')
    except (ValueError, TypeError):
        pass
    return redirect('cart:cart_detail')
