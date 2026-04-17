from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product


def home(request):
    categories = Category.objects.filter(parent=None)[:6]
    featured_products = Product.objects.filter(is_available=True).order_by('-views_count')[:8]
    new_products = Product.objects.filter(is_available=True).order_by('-created')[:8]
    return render(request, 'catalog/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'new_products': new_products,
    })


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.filter(parent=None)
    products = Product.objects.filter(is_available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    q = request.GET.get('q', '')
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))

    sort = request.GET.get('sort', '-created')
    allowed_sorts = ['price', '-price', '-views_count', '-created', 'created']
    if sort in allowed_sorts:
        products = products.order_by(sort)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'q': q,
        'sort': sort,
        'min_price': min_price or '',
        'max_price': max_price or '',
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)

    Product.objects.filter(pk=product.pk).update(views_count=product.views_count + 1)
    product.refresh_from_db()

    recently_viewed = request.session.get('recently_viewed', [])
    if product.id not in recently_viewed:
        recently_viewed.insert(0, product.id)
        recently_viewed = recently_viewed[:10]
        request.session['recently_viewed'] = recently_viewed

    recommended = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(pk=product.pk).order_by('-views_count')[:4]

    recently_viewed_products = Product.objects.filter(
        id__in=recently_viewed, is_available=True
    ).exclude(pk=product.pk)[:5]

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'recommended': recommended,
        'recently_viewed_products': recently_viewed_products,
    })
