# Create your views here.
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from pomodoro.utils import getTask, finishTask
import logging

log = logging.getLogger(__name__)

def do(request,pk):
    task = getTask(pk,request.user)
    if not task:
        return Http404
    return render_to_response("pomodoro-do.html",{'task':task},context_instance=RequestContext(request))

def finished(request,pk):
    task = getTask(pk,request.user)
    if not task:
        return Http404
    finished= finishTask(task)
    log.debug("finisehd ? %s",finished)
    return redirect(reverse("pomodoro-pause"))