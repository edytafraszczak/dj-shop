from django.db.models import Count, F

from .cart import Cart
from .models import Category


def categories(request):
    return {'categories': Category.objects.all().annotate(
        products_count=Count(F('products')))}


def cart(request):
    return {'cart': Cart(request)}
