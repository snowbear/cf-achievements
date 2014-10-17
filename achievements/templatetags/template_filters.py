import re
from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from achievements.models import *

register = template.Library()

def get_color_style(rating):
    if rating >= 2200:
        return "user-red"
    elif rating >= 1900:
        return "user-orange"
    elif rating >= 1700:
        return "user-violet"
    elif rating >= 1500:
        return "user-blue"
    elif rating >= 1200:
        return "user-green"
    else:
        return "user-gray"

def get_user_link(handle):
    user = Contestant.objects.get(handle = handle)
    cssClass = "";
    if user.rating != None:
        cssClass += " rated-user %s" % get_color_style(user.rating)
    return "<a href=\"%s\" class=\"%s\">%s</a>" % (reverse('achievements:profile', args=[handle]), cssClass, handle)

@register.filter()
def to_user_link(handle):
    return mark_safe(get_user_link(handle))
    
@register.filter()
def replace_tags(input):
    result = ""
    nextChar = 0
    for match in re.finditer(r"\[(contest|user):([^\]]+)\]", input):
        result += input[nextChar:match.span()[0]]
        if match.group(1) == "contest":
            contest = Contest.objects.get(pk = int(match.group(2)))
            result += contest.name
        elif match.group(1) == "user":
            handle = match.group(2)
            result += get_user_link(handle)
        nextChar = match.span()[1]
    result += input[nextChar:]
    return mark_safe(result)