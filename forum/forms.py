__author__ = 'Milena Farfulowska'

from django import forms
from forum.models import Thread, User, Response
from django.core.exceptions import ObjectDoesNotExist


class ThreadForm(forms.ModelForm):
    class Meta:
        model=Thread
        fields=('title','content','category')
        labels={
            'title': ('tytul'),
            'content': ('tresc'),
            'category': ('kategoria'),
        }

class UserForm1(forms.ModelForm):
    class Meta:
        model=User
        fields=['login', 'password']
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'login', 'required': '', 'autofocus':''}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password',
                                                             'placeholder': 'haslo', 'required': ''}))
    ban = forms.BooleanField(required=False)

class UserForm2(forms.ModelForm):
    class Meta:
        model=User
        fields=('login', 'email', 'password')
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'login', 'required': '', 'autofocus':''}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email',
                                                            'type': 'email', 'required': ''}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'haslo',
                                                            'type': 'password', 'required': ''})
        }
    confirmpassword = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password',
                                                            'placeholder': 'powtorz haslo','required': ''}))

class UserFormEdit(forms.ModelForm):
    class Meta:
        model=User
        fields=('login', 'email', 'password')
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'login', 'required': '', 'autofocus':''}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email',
                                                            'type': 'email', 'required': ''}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'haslo',
                                                            'type': 'password', 'required': ''})
        }

class UserFormAdmin(forms.ModelForm):
    class Meta:
        model=User
        fields=('login', 'email', 'ban', 'type')
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'login', 'required': '', 'autofocus':''}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email',
                                                            'type': 'email', 'required': ''}),
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model=Response
        fields=['content', 'user']
        labels={
            'content': ('tresc'),
            'user': ('uzytkownik'),
        }


