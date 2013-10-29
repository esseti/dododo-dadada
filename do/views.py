# Create your views here.
import calendar
from datetime import datetime, timedelta
import logging
from django.contrib import messages

from django.contrib.auth import logout
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.views.generic.base import View

from do.forms import TaskForm
from do.models import List, Task


log = logging.getLogger(__name__)


def getUser(request):
    log.debug("user %s", request.user.username)
    # user, created = User.objects.get_or_create(username="me", password="me")
    return request.user


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
        return int(e - today.day + e2), '#nm'
    else:
        return 0, ''


def parserTask(task):
    result = {}
    # find the list
    # list, s, e = findPart(task, "@")
    # task = task.replace(list, "")
    # list = list[1:]
    # log.debug("list %s", list)
    # find priority
    priority, s, e = findPart(task, "#p")
    task = task.replace(priority, "")
    priority = int(priority[2:3])
    log.debug("priority - %s", priority)
    days, kw = findDays(task)
    task = task.replace(kw, "")
    return (False, task, priority, days)


class ToDo(View):
    def get(self, request, *args, **kwargs):

        form = TaskForm()
        task_list = Task.objects.all().filter(list__owner=getUser(request))
        task_list_done = task_list.filter(done=True)
        task_list = task_list.filter(done=False)        # list = None
        # if "list" in kwargs:
        #     task_list = task_list.filter(list__title=str(kwargs['list']))
        #     form = TaskForm(initial={'task': ("@%s " % (kwargs['list']))})
        #     list = kwargs['list']
        sort = request.GET.get('sort', None)
        log.debug(sort)
        log.debug(sort is "priority")
        log.debug(sort is "deadline")

        if sort == "priority":
            task_list = sorted(task_list, key=lambda x: x.priority)
        elif sort == "deadline":
            task_list = sorted(task_list, key=lambda x: x.priority)
            task_list = sorted(task_list, key=lambda x: x.deadline)
        else:
            task_list = sorted(task_list, key=lambda x: x.weight, reverse=True)
        return render_to_response('list.html', {'task_list': task_list, 'task_list_done': task_list_done, 'form': form},
                                  context_instance=RequestContext(request))


def post(self, request, *args, **kwargs):
    user = getUser(request)
    log.debug("add task")
    task = request.POST['task']
    form = TaskForm(request.POST)
    if form.is_valid():
        log.debug("ok")
        error, task_title, priority, days = parserTask(task)
        log.debug("t: %s p:%s days:%s", task_title, priority, days)
        list, created = List.objects.get_or_create(owner=user, title="inbox")
        task = Task(title=task_title, priority=priority, list=list, deadline=datetime.now() + timedelta(days=days))
        task.save()
        messages.success(request, "Add task '%s' with priority %s due in %s days " % (task_title, priority, days))
        log.debug("task added %s", task.deadline)
        form = TaskForm()

    task_list = Task.objects.all().filter(list__owner=getUser(request))
    task_list_done = task_list.filter(done=True)
    task_list = task_list.filter(done=False)
    list = None
    # if "list" in kwargs:
    #     task_list = task_list.filter(list__title=str(kwargs['list']))
    #     list = kwargs['list']

    task_list = sorted(task_list, key=lambda x: x.weight, reverse=True)
    return render_to_response('list.html', {'task_list': task_list, 'task_list_done': task_list_done, 'form': form},
                              context_instance=RequestContext(request))




    # else:
    #     messages.error(request, 'Priority or List missed')

#TODO: strike done,
#TODO: visibility 0
#TODO: datetime of completition
def Done(request, pk):
    log.debug("pk %s", pk)
    task = get_object_or_404(Task, pk=pk, list__owner=request.user)
    task.done = not task.done
    task.save()
    done_or_not = "done" if task.done else "undone"
    messages.success(request, "Task %s %s" % (task.title, done_or_not))
    return redirect("/")


def logout_view(request):
    logout(request)
    return redirect("/")