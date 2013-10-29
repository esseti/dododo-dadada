from datetime import timedelta, date
import logging

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

log = logging.getLogger(__name__)


class List(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=255)


class Task(models.Model):
    title = models.CharField(max_length=255)
    list = models.ForeignKey(List)
    priority = models.SmallIntegerField(default=-1)
    deadline = models.DateField(auto_now=False)
    done = models.BooleanField(default=False)

    @property
    def deadline_type(self):
        deadline = self.deadline
        log.debug("%s %s", type(deadline), type(date.today()))
        if deadline - date.today() < timedelta(0):
            return (1, 'overdue')
        elif deadline - date.today() == timedelta(0):
            return (2, 'today')
        elif deadline - date.today() == timedelta(1):
            return (3, 'tomorrow')
        elif deadline.isocalendar()[1] - date.today().isocalendar()[1] == 0:
            return (4, 'this week')
        elif deadline.isocalendar()[1] - date.today().isocalendar()[1] == 1:
            return (5, 'next week')
        elif deadline.month == date.today().month:
            return (6, 'this month')
        else:
            return (7, 'next month')

    @property
    def weight(self):
        if self.done:
            return 0
        days = self.deadline_type[0]
        priority = self.priority
        w = ((10 - priority)) * (1.0 / float(days))
        if priority in [4, 5, 6]:
            w = w / (1.0 + (0.5 * ((2 + (priority - 6)) / 3.0)))
        elif priority in [7, 8, 9]:
            w = w / (2.0 + (0.5 * ((2 + (priority - 9)) / 3.0)))

        return w


class SubTask(models.Model):
    title = models.CharField(max_length=255)
    # list = models.ForeignKey(List)
    # priority = models.SmallIntegerField(default=-1)
    # deadline = models.DateField(auto_now=False)
    done = models.BooleanField(default=False)
    task = models.ForeignKey(Task)