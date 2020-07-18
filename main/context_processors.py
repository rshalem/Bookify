"""
common contexts goes here, registerd at settings.py
"""

from .models import Genre, OrderItem

def genres(request):

    all_genre = Genre.objects.all()

    total_cart_items = 0
    all_order_item = OrderItem.objects.all()
    total_cart_items = 0
    for item in all_order_item:
        total_cart_items += item.quantity

    return {'all_genres': all_genre, 'item_count': total_cart_items}
