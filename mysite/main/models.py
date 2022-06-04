from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(default='user_default.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    is_seller = models.BooleanField(default=False)
    books_sale = models.TextField(default="")

    def __str__(self):
        return self.name


class Book(models.Model):
    seller = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, null=True, unique=True)
    author = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=800, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    picture = models.ImageField(null=True, blank=True)
    book_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name


class BooksHave(models.Model):
    owner = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.name

