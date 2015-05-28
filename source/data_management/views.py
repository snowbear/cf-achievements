import datetime
import json

from django.db import connection
from django.db.models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from achievements.models import *
from achievements.achievement_data import *
from data_management.models import *

@login_required
def index(request):
    last_contest = Contest.objects.order_by('-order').first()
    
    achievements = [{'achievement': a, 'last_parsed': AchievementParseProgress_ByContest.get_for_achievement(a.id)} for a in Achievement.objects.all()]
    
    for ach in achievements:
        ach['needs_update'] = ach['last_parsed'].lastParsedContest != last_contest
    
    return render(request,
                  'data_management/index.html', {
                      'last_contest': last_contest,
                      'achievements': achievements,
                    });
