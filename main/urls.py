from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('search/', views.search_query, name='search'),
    path('cart/', views.cart, name='cart'),
    path('checkout/address', views.add_address, name='address'),
    path('checkout/payment/', views.payment, name='payment'),

    path('add/<book_slug>', views.add_to_cart, name='add-to-cart'),
    path('detail/<book_slug>/', views.book_detail, name='detail'),
    path('genre/<genre_name>/', views.genre, name='genre'),

]
