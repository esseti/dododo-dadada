'''
Created on Oct 9, 2012

@author: stefanotranquillini
'''
from datetime import datetime
import logging
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


log = logging.getLogger(__name__)
@stringfilter
@register.filter(name='trans_task')
def trans_task(task):
    log.debug(task.priority)

    total = float(11-task.priority)/10.0
    return total+0.1

@stringfilter
@register.filter(name='mynaturalday')
def mynaturalday(deadline):
    log.debug(deadline)
    # return deadline
    today = datetime.today()
    log.debug(deadline.weekday)
    # deadline = datetime.strptime(str(deadline), '%d-%m-%y').date()
    if deadline.weekday() - today.weekday() == 0:
        return 'today'
    elif deadline.weekday()-today.weekday() == 1:
        return 'tomorrow'
    elif deadline.isocalendar()[1]-today.isocalendar()[1] == 0:
        return 'this week'
    elif deadline.isocalendar()[1]-today.isocalendar()[1] == 1:
        return 'next week'
    elif deadline.month  == today.month:
        return 'this month'
    else:
        return 'next month'

@register.filter(name='to_tr_class')
def toTrClass(value):
    # txt = mynaturalday(value)
    switch = {
        'today': 'danger',
        'tomorrow': 'warning',
        'this week': 'success',
        'next week': 'primary',
        'this month': 'info',
        'next month': 'default'
    }
    res = switch[value]
    log.debug("%s->%s",value,res)
    return res