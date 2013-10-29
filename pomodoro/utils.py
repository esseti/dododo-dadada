__author__ = 'stefanotranquillini'
from do.models import Task

def getTask(pk,user):
    return Task.objects.get(pk=pk, list__owner=user)

def finishTask(task):
    prev = task.done
    task.done = not task.done
    task.save()
    return task.done != prev