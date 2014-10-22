import re

from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from achievements.models import *

register = template.Library()

def get_color_style(rating):
    if rating == None:
        return "user-black"
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

def link(destination, text, cssClass = None):
    classAttribute = ""
    if cssClass != None:
        classAttribute = "class='%s'" % cssClass;
    return "<a href='%s' %s>%s</a>" % (destination, classAttribute, text)
        
def get_user_link(user):
    if type(user) is str:
        user = Contestant.objects.get(handle = user)
    cssClass = "rated-user %s" % get_color_style(user.rating)
    return link(reverse('achievements:profile', args=[user.handle]), user.handle, cssClass)

@register.filter()
def to_user_link(user):
    return mark_safe(get_user_link(user))

def get_contest_link(contestId):
    contest = Contest.objects.get(pk = contestId)
    return link(reverse('achievements:contest', args=[contestId]), contest.name, 'contest-link')

@register.filter()
def to_achievement_link(achievement):
    return mark_safe(link('#', achievement.name, 'achievement-link'))

@register.filter()
def replace_tags(input):
    result = ""
    nextChar = 0
    for match in re.finditer(r"\[(contest|user):([^\]]+)\]", input):
        result += input[nextChar:match.span()[0]]
        if match.group(1) == "contest":
            contestId = int(match.group(2))
            result += get_contest_link(contestId)
        elif match.group(1) == "user":
            handle = match.group(2)
            result += get_user_link(handle)
        nextChar = match.span()[1]
    result += input[nextChar:]
    return mark_safe(result)