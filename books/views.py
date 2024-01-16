from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import forms, models
from accounts.models import UserLibraryAccount
from decimal import Decimal
from transactions.models import Transaction
from transactions.constants import BORROWED, RETURNED
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_borrow_email(user, amount, subject, template, current_balance):
    message = render_to_string(template, {'user': user,'amount': amount,'current_balance': current_balance,})
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()


def details_book(request, book_id):
    book = get_object_or_404(models.Book, id=book_id)
    user = request.user

    if request.method == 'POST':

        if 'borrow_now' in request.POST:
         if user.is_authenticated:
           
            user_account = UserLibraryAccount.objects.filter(user=user).first()

            if not user_account:
                messages.error(
                    request, 'You need a library account to borrow books. Please create an account.')
                return redirect('details_book', book_id=book.id)


            if user_account.balance < book.price:
                messages.error(
                    request, 'You do not have enough balance to borrow this book.')
                return redirect('details_book', book_id=book.id)

            user_account.balance = user_account.balance - Decimal(str(book.price))
            user_account.save()

            Transaction.objects.create( account=user_account,amount=-book.price,balance_after_transaction=user_account.balance,transaction_type=BORROWED)
            send_borrow_email(user, book.price, 'Borrow Message','books/borrow_email.html', user_account.balance)
            
            book.borrowers.add(user)


            messages.success(request, 'Book Borrowed Successfully!')
            return redirect('details_book', book_id=book.id)
         

        elif 'return_book' in request.POST:
            user_account = UserLibraryAccount.objects.filter(user=user).first()
            if not user_account:
                messages.error(
                    request, 'No account found! You need a library account to borrow books. Please create an account.')
                return redirect('details_book', book_id=book.id)
            
            user_account.balance += Decimal(str(book.price))
            user_account.save()

            Transaction.objects.create(account=user_account,amount=+book.price, balance_after_transaction=user_account.balance,transaction_type=RETURNED)
            book.borrowers.remove(user)
            messages.success(request, 'Book Returned Successfully!')


        elif 'comment' in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.book = book
                new_comment.save()

                messages.success(request, 'Comment Added Successfully.')

                
                print("Comment added successfully.")
                print(f"Redirecting to details_book page for book ID: {book.id}")

               
                return redirect('details_book', book_id=book.id)
        else:
            messages.error(
                request, 'You need to be logged in to borrow books.')
            return redirect('user_login')


    comments = models.Comment.objects.filter(book=book)
    comment_form = forms.CommentForm(initial={'user': user})


    return render(request, 'books/details_book.html', {'book': book, 'comments': comments, 'comment_form': comment_form})