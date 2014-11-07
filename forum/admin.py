__author__ = 'Milena Farfulowska'

from django.contrib import admin
from forum.models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Response)
admin.site.register(Rating)

