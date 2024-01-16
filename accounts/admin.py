from django.contrib import admin
from .models import UserLibraryAccount, UserAddress
# Register your models here.

admin.site.register(UserLibraryAccount)
admin.site.register(UserAddress)