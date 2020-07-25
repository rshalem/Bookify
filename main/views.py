from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404
from django.db.models import Q
from django.db import IntegrityError

from .models import *
from .forms import AddressForm


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
    username = request.POST.get('username')
    email = request.POST.get('email')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if request.method == 'POST':
        if password1 == password2:
            if password1 and password2 != username:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password2)
                    user.save()
                    return redirect('main:home')

                except IntegrityError:
                    return render(request, 'signup.html', {'error': "User already been taken"})
            else:
                return render(request, 'signup.html', {'error': 'Username & password should not match'})
        else:
            return render(request, 'signup.html', {'error': "Password didn't match"})

    return render(request, 'signup.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
        else:
            return render(request, 'login.html', {'error': 'User does not exists'})

    return render(request, 'login.html')


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


@login_required(login_url='/login/')
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST or None)
        if form.is_valid():
            # returns cleaned data & calls clean <field_name> validators
            obj = form.save(commit=False)
            obj.shipping_user = request.user
            obj.save()
            return redirect('main:payment')

        return render(request, 'address.html', {'error': form.errors, 'form': form})

    else:
        form = AddressForm()

    context = {'form': form}

    return render(request, 'address.html', context)


def payment(request):
    return render(request, 'payment.html')
