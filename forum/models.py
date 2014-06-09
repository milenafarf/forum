from django.db import models

class User(models.Model):
    login = models.CharField(max_length = 64)
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


class Thread(models.Model):
    title = models.CharField(max_length = 64)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category)
    thumbs_up = models.IntegerField()
    thumbs_down = models.IntegerField()


class Message(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    thumbs_up = models.IntegerField()
    thumbs_down = models.IntegerField()
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(User)