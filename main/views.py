from django.shortcuts import render, Http404
from django.db.models import Q

from .models import *

def homepage(request):
    try:
        book = Book.objects.all()
        genre = Genre.objects.all()
    except Book.DoesNotExist:
        raise Http404

    context = {'books': book,
               'genres': genre
               }
    return render(request, 'home.html', context=context)

def book_detail(request, book_slug):
    try:
        single_book_by_slug = Book.objects.get(book_slug=book_slug)
        genre = single_book_by_slug.genre
        books_related_to_genre = genre.genres.all()
    except Book.DoesNotExist:
        raise Http404

    context = {'book': single_book_by_slug,
               'book_for_genre': books_related_to_genre,
               }
    return render(request, 'book_detail.html', context=context)

def search_query(request):
    print(request.POST)
    search_request = request.POST['search_query']
    try:
        book = Book.objects.filter(Q(book_name__startswith=search_request) | Q(author__startswith=search_request))
    except Book.DoesNotExist:
        raise Http404

    context = {'books': book}

    return render(request, 'home.html', context)


def user_signup(request):
    return render(request, 'signup.html')
