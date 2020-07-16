from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('signup/', views.user_signup, name='signup'),
    path('search/', views.search_query, name='search'),
    path('cart/', views.cart, name='cart'),
    path('detail/<book_slug>/', views.book_detail, name='detail'),
    path('genre/<genre_name>/', views.genre, name='genre'),

]
