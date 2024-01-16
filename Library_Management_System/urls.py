
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('books_filter/<slug:book_category>', home, name='books_filter'),
    path('books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
    path('transactions/', include('transactions.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)