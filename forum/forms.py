__author__ = 'Milena Farfulowska'

from django import forms
from forum.models import Thread, User
from django.core.exceptions import ObjectDoesNotExist


class ThreadForm(forms.ModelForm):
    class Meta:
        model=Thread
        fields=('title','content','category', 'user')
        labels={
            'title': ('tytul'),
            'content': ('tresc'),
            'category': ('kategoria'),
            'user': ('uzytkownik'),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model=User