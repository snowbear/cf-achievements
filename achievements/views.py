from django.shortcuts import render
from django.http import HttpResponse

from achievements.models import *

def index(request):
    last_achievements = Rewarding.objects.order_by("-date")[:20]
    return render(request,
                  'achievements/index.html', {
                        'last_achievements': last_achievements,
                  })

def profile(request, handle):
    contestant = Contestant.objects.get(handle = handle)
    last_achievements = Rewarding.objects.filter(participant = contestant).order_by("-date")[:20]
    return render(request,
                  'achievements/profile.html', {
                        'last_achievements': last_achievements,
                  })

def contest(request, contestId):
    contest = Contest.objects.get(pk = contestId)
    achievements = Rewarding.objects.filter(contest = contest).order_by("-date")
    return render(request,
                  'achievements/contest.html', {
                        'contest': contest,
                        'achievements': achievements,
                  })
    return HttpResponse("112")