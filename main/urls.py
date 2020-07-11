from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('signup/', views.user_signup, name='signup'),
    path('search/', views.search_query, name='search'),
    path('detail/<book_slug>/', views.book_detail, name='detail'),

]
