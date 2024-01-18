from django.shortcuts import render
from django.views.generic import TemplateView
from books.models import Book
from books.constants import CATEGORY_CHOICES
# Create your views here.

def home(request, book_category=None):
    books = Book.objects.all()
    categories = [category[0] for category in CATEGORY_CHOICES]
    for book in books: 
        print(book)
    bookCategory = book_category
    if book_category:
        books = books.filter(categories=bookCategory)
     
    return render(request, 'index.html', {'books': books, 'categories': categories})