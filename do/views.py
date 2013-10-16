# Create your views here.
import calendar
from datetime import datetime, timedelta
import logging

from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.list import ListView
from django.views.generic.base import View

from do.forms import TaskForm
from do.models import List, Task


log = logging.getLogger(__name__)


def getUser():
    user, created = User.objects.get_or_create(username="me", password="me")
    return user


class TaskList(ListView):
    model = Task
    template_name = 'list.html'

    def get_queryset(self):
        # todo: for the list self.kwargs['process_id']

        log.debug("List length %s", len(task_list))
        return task_list


def findPart(s, c):
    posc = s.find(c)
    if posc == -1:
        return (None, None, None)
    log.debug("posc %s", posc)
    poss = s.find(" ", posc)
    poss = poss if poss > 0 else len(s)
    log.debug("poss %s", poss)
    res = s[posc:poss]
    log.debug("%s %s %s %s", s, posc, poss, res)
    return (res, posc, poss)


def findDays(task):
    today = datetime.today()
    if task.find("#td") > -1:
        return 0, '#td'
    elif task.find("#tm") > -1:
        return 1, '#tm'
    elif task.find('#tw') > -1:
        return 6 - today.weekday(), '#tw'
    elif task.find('#nw') > -1:
        return (7 - today.weekday()) + 6, '#nw'
    elif task.find('#mo') > -1:
        e = calendar.monthrange(today.year, today.month)[1]
        return e - today.day, '#mo'
    elif task.find('#nm') > -1:
        e = calendar.monthrange(today.year, today.month)[1]
        if today.month == 12:
            m = 1
            y = today.year + 1
            e2 = calendar.monthrange(y, m)[1]
        else:
            e2 = calendar.monthrange(today.year, today.month)[1]
        return int(e - today.day + e2 ), '#nm'
    else:
        return 0, ''


def parserTask(task):
    result = {}
    # find the list
    list, s, e = findPart(task, "@")
    task = task.replace(list, "")
    list = list[1:]
    log.debug("list %s", list)
    # find priority
    priority, s, e = findPart(task, "#p")
    task = task.replace(priority, "")
    priority = int(priority[2:])
    log.debug("priority - %s", priority)
    days, kw = findDays(task)
    task = task.replace(kw, "")
    return (False, task, priority, list, days)


class ToDo(View):
    def get(self, request, *args, **kwargs):

        form = TaskForm()
        task_list = Task.objects.all().filter(list__owner=getUser()).order_by('deadline').order_by('priority')
        list = None
        if "list" in kwargs:
            task_list = task_list.filter(list__title=str(kwargs['list']))
            form = TaskForm(initial={'task': ("@%s " % (kwargs['list']))})
            list = kwargs['list']

        return render_to_response('list.html', {'task_list': task_list, 'form': form, 'list': list},
                                  context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        user = getUser()
        log.debug("add task")
        task = request.POST['task']
        form = TaskForm(request.POST)
        if form.is_valid():
            log.debug("ok")
            error, task_title, priority, list_title, days = parserTask(task)
            log.debug("t: %s p:%s l:%s", task_title, priority, list_title)
            list, created = List.objects.get_or_create(owner=user, title=list_title)
            task = Task(title=task_title, priority=priority, list=list, deadline=datetime.now() + timedelta(days=days))
            task.save()
            log.debug("task added")
            if "list" in kwargs:
                form = TaskForm(initial={'task': ("@%s " % (kwargs['list']))})
            else:
                form = TaskForm()

        task_list = Task.objects.all().filter(list__owner=getUser()).order_by('deadline').order_by('priority')
        list = None
        if "list" in kwargs:
            task_list = task_list.filter(list__title=str(kwargs['list']))
            list = kwargs['list']
        return render_to_response('list.html', {'task_list': task_list, 'form': form, 'list': list},
                                  context_instance=RequestContext(request))




        # else:
        #     messages.error(request, 'Priority or List missed')
