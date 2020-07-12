from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

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
