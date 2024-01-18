from django.shortcuts import render, redirect
from django.views.generic import FormView
from . forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
from books.models import Book
from transactions.models import Transaction
from transactions.constants import BORROWED

from .models import UserLibraryAccount
# Create your views here.



class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/registration.html'

    def form_valid(self, form):
        user = form.save()
        print(user)
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('profile')


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserProfileView(LoginRequiredMixin,View):
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
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('home')
        else:
            print(form.errors)
       
       
        return render(request, self.template_name, {'form': form})
       

class UserProfileUpdateView(LoginRequiredMixin,View):
    template_name = 'accounts/update_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user) 
        return render(request, self.template_name, {'form': form})


    def post(self, request):  
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            print(form.errors)

def change_pass(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, 'Your password was successfully updated!')
                
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')
        return render(request, 'accounts/form.html', {'form': form, 'title': ' You can change password', 'button_text': 'Change Password', 'button_class': 'btn-warning'})
    else:
        return redirect('home')