from .models import Category


def categories(request):
    return {'all_categories': Category.objects.filter(parent=None).prefetch_related('children')}
