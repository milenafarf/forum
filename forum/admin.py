__author__ = 'Milena'

from django.contrib import admin
from forum.models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Message)

