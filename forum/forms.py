__author__ = 'Milena Farfulowska'

from django import forms
from forum.models import Thread, User, Response, Category
from django.core.exceptions import ObjectDoesNotExist


class ThreadForm(forms.ModelForm):
    class Meta:
        model=Thread
        fields=('title','content','category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': '', 'autofocus':''}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'required': ''}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': ''})
        }



#used while signing in
class UserForm1(forms.ModelForm):
    class Meta:
        model=User
        fields=['login', 'password']
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'login', 'required': '', 'autofocus':''}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password',
                                                             'placeholder': 'haslo', 'required': ''}))
    rememberMe = forms.BooleanField(required=False)

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
                                                            'type': 'password', 'required': ''}),
            # 'ban': forms.BooleanField(attrs={'class': 'form-control'}),

        }

class UserFormAdmin(forms.ModelForm):
    class Meta:
        model=User
        fields=('login', 'email', 'ban', 'type')
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'login', 'required': '', 'autofocus':''}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email',
                                                            'type': 'email', 'required': ''}),
            # 'ban': forms.CheckboxInput(attrs={'class': 'form-control'})
            'type': forms.Select(attrs={'class': 'form-control'})
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model=Response
        fields=['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control','rows':'5', 'required': '', 'autofocus':''})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': '', 'autofocus':''})
        }
