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
    if request.user.users_agent.form_state[pattern] == 1:
        return 'bg-success progtrckr-done'
    else:
        return 'bg-danger progtrckr-todo'
