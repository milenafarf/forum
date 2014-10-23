__author__ = 'Milena Farfulowska'

from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField


class User(models.Model):
    login = models.CharField(max_length = 64)
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True) #Automatically set the field to now
                                    # when the object is first created. Useful for creation of timestamps
    last_update = models.DateTimeField(auto_now=True)
    ban = models.BooleanField(default=False)
    def __unicode__ (self):
        return self.login


class Category(models.Model):
    name = models.CharField(max_length = 64)
    def __unicode__ (self):
        return self.name


class Thread(models.Model):
    title = models.CharField(max_length = 64)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category)
    rating = ListField(EmbeddedModelField('Rating'), null=True)
    user = models.ForeignKey(User)
    def __unicode__ (self):
        return self.title


class Message(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    rating = ListField(EmbeddedModelField('Rating'),null=True)
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(User)


class Rating(models.Model):
    thumb_up = models.BooleanField() #thumb_up --> true, thumb_down--> false
    user = models.ForeignKey(User)
