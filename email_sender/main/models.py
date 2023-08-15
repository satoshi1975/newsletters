"""models"""
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Subscriber(models.Model):
    """User subscriber model"""
    user = models.ForeignKey(User, on_delete = models.CASCADE,default = None)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    date_of_birth = models.DateField()

    def __str__(self):
        return self.email

class SentMessage(models.Model):
    """model of the message that was sent"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    recipient = models.ForeignKey(Subscriber, on_delete=models.CASCADE,default=None, null=True)
    status = models.CharField(max_length = 20,default = None, null=True)
    message = models.TextField(default = None, null=True)
    track_num = models.BigIntegerField(default= None, blank = True, null=True)
    
    def __str__(self):
        return self.recipient
