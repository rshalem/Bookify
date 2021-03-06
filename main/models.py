from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField


class Address(models.Model):
    shipping_user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_first_name = models.CharField(max_length=20)
    shipping_last_name = models.CharField(max_length=20)
    shipping_house_no = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=12, default='')
    shipping_user_email = models.EmailField(max_length=50, default='')
    shipping_address_one = models.CharField(max_length=50)
    shipping_address_two = models.CharField(max_length=50, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=20)
    shipping_country = CountryField(multiple=False)
    shipping_zip = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.shipping_first_name}, {self.shipping_address_one.split(',')[0]}"


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

    # Meta class of the model, for permissions to a given set of users or groups
    class Meta:
        # can only add, not change or delete
        default_permissions = ('add',)

        # adding custom permissions
        permissions = (('can_add_genre', 'Add a genre'),)

    def __str__(self):
        return self.genre_name


class Location(models.Model):
    city_name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name


class Language(models.Model):
    language_name = models.CharField(max_length=50)

    def __str__(self):
        return self.language_name


class Book(models.Model):
    book_name = models.CharField(max_length=50)
    book_image = models.ImageField(blank=True, null=True)
    author = models.CharField(max_length=50)
    book_description = models.TextField()
    isbn_no = models.IntegerField(blank=True)
    price = models.FloatField()
    rating = models.FloatField()
    availability = models.BooleanField(default=True)
    genre = models.ForeignKey(Genre, related_name='genres', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_name='place', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_upload', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, related_name='lang_books', on_delete=models.CASCADE)
    book_slug = models.SlugField(max_length=50, unique=True, default='')

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return self.book_name

    def is_available(self):
        if self.availability:
            return True
        else:
            return False

    @property
    def imgURL(self):
        try:
            url = self.book_image.url
        except:
            url = ''
        return url

    def get_absolute_url(self):
        return reverse('main:detail', kwargs={'book_slug': self.book_slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.book_slug = slugify(self.book_name)
        super(Book, self).save(*args, **kwargs)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_content = models.TextField()
    review_date = models.DateField()
    rating_star = models.FloatField()

    def __str__(self):
        return self.review_content[:10]


class OrderItem(models.Model):
    # OrderItem = BookItem
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.book.book_name

    @property
    def total_price(self):
        if self.id:
            total = self.quantity * self.book.price
        else:
            total = 0
        return total


class Payment(models.Model):

    payment_choices = [
        ('S', 'Stripe'),
        ('P', 'Paytm'),
    ]

    payment_mode = models.CharField(max_length=6, choices=payment_choices, default='S')
    transaction_id = models.CharField(max_length=50, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.FloatField(default=0)
    transaction_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"User name: {self.user.username} | Transaction id: {self.transaction_id}"


# cart
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"Order object {str(self.id)}"

    def cart_total(self):
        total_cart_value = 0
        for item in self.order_item.all():
            total_cart_value += item.total_price
        return total_cart_value

    def order_status_complete(self):
        self.complete = True
        return self.complete
