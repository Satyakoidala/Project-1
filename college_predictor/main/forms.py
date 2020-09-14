from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Firstname'
    }) ,max_length=30, help_text='Required.')
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Lastname'
    }) ,max_length=30, help_text='Required.')
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder':'Email'
    }) ,max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'COnfirm Password'}),
        }