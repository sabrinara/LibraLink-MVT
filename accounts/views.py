from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from books.models import Book
from transactions.models import Transaction
from transactions.constants import BORROWED
from .models import UserLibraryAccount
import logging

logger = logging.getLogger(__name__)

class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration.html'

    def form_valid(self, form):
        user = form.save()
        logger.debug(f"User registered: {user}")
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.debug(f"Registration form invalid: {form.errors}")
        return super().form_invalid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def form_valid(self, form):
        logger.debug("User login successful")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.debug(f"User login failed: {form.errors}")
        return super().form_invalid(form)

    def get_success_url(self):
        logger.debug("User login redirect to profile")
        return reverse_lazy('profile')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        logger.debug("User logout")
        return super().dispatch(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        borrowers = Book.objects.filter(borrowers=request.user)
        transaction_history = Transaction.objects.filter(
            account=request.user.account,
            transaction_type=BORROWED
        ).order_by('-timestamp')
        return render(request, self.template_name, {'form': form, 'books': borrowers, 'transaction_history': transaction_history})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('home')
        else:
            logger.debug(f"Profile update form invalid: {form.errors}")
        return render(request, self.template_name, {'form': form})

class UserProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'accounts/update_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            logger.debug(f"Profile update form invalid: {form.errors}")

def change_pass(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
        return render(request, 'accounts/form.html', {'form': form, 'title': 'You can change password', 'button_text': 'Change Password', 'button_class': 'btn-warning'})
    else:
        return redirect('home')
