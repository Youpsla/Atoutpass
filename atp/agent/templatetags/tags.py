# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.simple_tag
def active(request, pattern):
    if request.path.startswith(pattern):
        return 'active'
    return ''


@register.simple_tag
def switch_state(request, pattern):
    print request.user.agent.form_state[pattern]
    if request.user.agent.form_state[pattern] == 1:
        return 'completed'
    else:
        return ''
