from django.urls import path
from . import views

urlpatterns = [
    path('details_book/<int:book_id>/', views.details_book, name='details_book'),
]