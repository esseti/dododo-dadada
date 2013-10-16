from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class List(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255)

class Task(models.Model):
    title = models.CharField(max_length=255)
    list = models.ForeignKey(List)
    priority = models.SmallIntegerField(default=-1)
    deadline = models.DateField(auto_now=False)