from django.urls import path
from . views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileView, change_pass, UserProfileUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update_profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('change_pass/', change_pass, name='change_pass'),
]