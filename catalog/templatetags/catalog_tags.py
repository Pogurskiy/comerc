from django import template

register = template.Library()


@register.filter
def discount_price(product):
    return product.get_discounted_price()


@register.filter
def discount_percent(product):
    return product.get_discount_percent()


@register.simple_tag
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
