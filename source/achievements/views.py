import json

from collections import defaultdict
from itertools import *

from django.core.urlresolvers import reverse
from django.db.models import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from achievements.models import *
from achievements.achievement_data import *

def index(request):
    last_achievements = Rewarding.objects.order_by("-date")[:20]
    achievements = Achievement.objects.annotate(total = Count('rewarding')).order_by("name")
    return render(request,
                  'achievements/index.html', {
                        'last_achievements': last_achievements,
                        'achievements': achievements,
                  })

def to_stat_row(achievement, grouped_rewardings):
    latest_rewarding = None
    total_count = 0
    if grouped_rewardings[achievement.id] != None:
        rewardings = grouped_rewardings[achievement.id]
        latest_rewarding = max(rewardings, key=lambda rewarding: rewarding.date)
        total_count = len(rewardings)
    return (achievement, latest_rewarding, total_count)
                  
def profile(request, handle):
    contestant = Contestant.objects.get(handle = handle)
    achievements = Rewarding.objects.filter(participant = contestant).order_by("-date")
    
    by_achievement = lambda rewarding: rewarding.achievement.id
    grouped_rewardings = defaultdict(lambda: None)
    for k, g in groupby(sorted(achievements, key=by_achievement), by_achievement):
        grouped_rewardings[k] = list(g)
    
    achievements_unlocked = len(grouped_rewardings)
    
    all_achievements = Achievement.objects.order_by("name")
    all_achievements = [ to_stat_row(a, grouped_rewardings) for a in all_achievements]
    
    return render(request,
                  'achievements/profile.html', {
                        'user': contestant,
                        'achievements': achievements,
                        'achievements_unlocked': achievements_unlocked,
                        'all_achievements': all_achievements,
                  })

def contest(request, contestId):
    contest = Contest.objects.get(pk = contestId)
    achievements = Rewarding.objects.filter(contest = contest).order_by("-date")
    return render(request,
                  'achievements/contest.html', {
                        'contest': contest,
                        'achievements': achievements,
                  })

def achievement(request, achievementId):
    achievement = Achievement.objects.get(pk = achievementId)
    latest_rewardings = Rewarding.objects.filter(achievement = achievement).order_by("-date")[:50]
    by_number = Rewarding.objects.filter(achievement = achievement).values('participant') \
                                    .annotate(count = Count('id'), first_date = Min('date')) \
                                    .order_by('-count')[:20]
    context = {
                        'achievement': achievement,
                        'latest_rewardings': latest_rewardings,
                        'by_number': by_number,
              }
    if achievement.id == POLYGLOT.id:
        context['by_level'] = Rewarding.objects.filter(achievement = achievement) \
                                    .order_by('-level', 'date')[:30]
    return render(request, 'achievements/achievement.html', context)

def search_user(request):
    term = request.GET['term']
    matching_users = Contestant.objects.filter(handle__icontains = term).order_by("handle")
    if request.GET.get("ajax", "") == "true":
        handles = [u.handle for u in matching_users[:20]]
        return HttpResponse(json.dumps(handles))
    else:
        for user in matching_users:
            if user.handle == term:
                return HttpResponseRedirect(reverse('achievements:profile', args=[user.handle]))
        return render(request,
                      'achievements/search_user.html', {
                            'matching_users': matching_users,
                            'query': term,
                      })