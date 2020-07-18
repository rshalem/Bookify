from django.contrib import messages
from django.shortcuts import render, redirect, Http404
from django.db.models import Q

from .models import *


def homepage(request):
    try:
        book = Book.objects.all()
    except Book.DoesNotExist:
        raise Http404

    context = {'books': book}
    return render(request, 'home.html', context=context)

def genre(request, genre_name):
    try:
        books_related_to_genre = Book.objects.filter(genre__genre_name=genre_name)
    except Book.DoesNotExist:
        raise Http404

    context = {'books': books_related_to_genre}
    return render(request, 'home.html', context=context)


def book_detail(request, book_slug):
    try:
        single_book_by_slug = Book.objects.get(book_slug=book_slug)
        reviews = single_book_by_slug.review_set.all()
        books_related_to_genre = single_book_by_slug.genre.genres.all().exclude(book_name=single_book_by_slug.book_name)
        # single_book_by_slug.genre.book_set.all()

    except Book.DoesNotExist:
        raise Http404

    context = {'book': single_book_by_slug,
               'book_for_genre': books_related_to_genre,
               'reviews': reviews,
               }
    return render(request, 'book_detail.html', context=context)

# SEARCH BLOCK CODE ---
def isbn_search_is_number(value):
    # for checking whether the entered search is by isbn and all digits

    for i in range(len(value)):
        if str(value[i]).isdigit() != True:
            return False
    return True

def search_query(request):

    search_request = request.GET['search_query']

    if isbn_search_is_number(search_request):
        book = Book.objects.filter(isbn_no__exact=search_request)
    else:
        try:
            book = Book.objects.filter(Q(book_name__startswith=search_request) | Q(author__startswith=search_request))
        except Book.DoesNotExist:
            raise Http404

    context = {'books': book}

    return render(request, 'home.html', context)

# --- SEARCH BLOCK ENDS

def user_signup(request):
    return render(request, 'signup.html')

def add_to_cart(request, book_slug):
    single_book_slug = Book.objects.get(book_slug=book_slug)
    # getting first matched obj and returns queryset
    order_item = OrderItem.objects.filter(book__book_slug=single_book_slug.book_slug).first()

    if order_item is not None:
        order_item.quantity += 1
        order_item.save()
    else:
        OrderItem.objects.create(book=single_book_slug, quantity=1)

    return redirect('main:cart')


def cart(request):
    all_order_items = OrderItem.objects.all()
    total_cart_items = 0
    for item in all_order_items:
        total_cart_items += item.quantity

    context = {'order_items': all_order_items,
               'total_items': total_cart_items}

    return render(request, 'cart.html', context)

def checkout(request):
    return render(request, 'checkout.html')
