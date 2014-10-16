import re
from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from achievements.models import *

register = template.Library()

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
            replacement = "<a href=\"%s\">%s</a>" % (reverse('achievements:profile', args=[handle]),
                                                     handle)
            result += replacement
        nextChar = match.span()[1]
    result += input[nextChar:]
    return mark_safe(result)