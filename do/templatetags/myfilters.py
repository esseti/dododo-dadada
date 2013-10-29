'''
Created on Oct 9, 2012

@author: stefanotranquillini
'''
from datetime import datetime, timedelta
import logging
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

log = logging.getLogger(__name__)


@stringfilter
@register.filter(name='trans_task')
def trans_task(task):
    log.debug(task.priority)

    total = float(11 - task.priority) / 10.0
    return total + 0.1

@stringfilter
@register.filter(name='to_tr_class')
def toTrClass(value):
    # txt = mynaturalday(value)
    switch = {
        1: 'danger',
        2: 'danger',
        3: 'warning',
        4: 'success',
        5: 'primary',
        6: 'info',
        7: 'default'
    }
    res = switch[value]
    return res