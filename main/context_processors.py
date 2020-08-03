"""
common contexts goes here, registerd at settings.py
"""
from django.contrib.auth.models import User
from .models import Genre, OrderItem

def genres(request):

    all_genre = Genre.objects.all()

    if request.user.is_authenticated:
        all_order_item = OrderItem.objects.filter(user=request.user or None)

    else:
        all_order_item = OrderItem.objects.all()

    total_cart_items = 0
    for item in all_order_item:
        total_cart_items += item.quantity

    return {'all_genres': all_genre, 'item_count': total_cart_items}
