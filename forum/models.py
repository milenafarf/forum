from django.db import models

class User(models.Model):
    login = models.CharField(max_length = 64)
    firstname = models.CharField(max_length = 64)
    lastname = models.CharField(max_length = 64)
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True) #Automatically set the field to now
                                    # when the object is first created. Useful for creation of timestamps
    last_update = models.DateTimeField(auto_now=True)
    ban = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length = 64)
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class Forum(models.Model):
    name = models.CharField(max_length = 64)
    desc = models.CharField(max_length = 256) #short description of forum
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category)

class Message(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    forum = models.ForeignKey(Forum)