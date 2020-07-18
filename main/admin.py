from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'author', 'rating', 'genre', 'isbn_no', 'availability',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity',)


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(Language)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
