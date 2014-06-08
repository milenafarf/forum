__author__ = 'Milena'

from django.contrib import admin
from forum.models import *

admin.site.register(Forum)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Message)