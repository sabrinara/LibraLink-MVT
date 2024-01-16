from django import forms
from . import models

class bookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['categories', 'title','image', 'description',  'price']


class CommentForm(forms.ModelForm):
   
    class Meta:
        model = models.Comment
        fields = ['name', 'email', 'body']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['name'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
        elif self.instance and not self.instance.user:
            user = self.initial.get('user')
            if user and user.is_authenticated:
                self.fields['name'].initial = user.username
                self.fields['email'].initial = user.email