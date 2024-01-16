from django.db import models
from django.contrib.auth.models import User
from .constants import CATEGORY_CHOICES
# Create your models here.


class Book(models.Model):
    categories = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='books/media/uploads', blank=True, null=True)
    description = models.TextField()
    price = models.FloatField()  
    borrowers = models.ManyToManyField(User, related_name='borrowed_books', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)