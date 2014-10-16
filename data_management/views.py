import datetime
import json

from django.db import connection
from django.db.models import Min
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from achievements.models import *
from achievements.achievement_data import *
from data_management.models import *

def index(request):
    last_contest = Contest.objects.order_by('-date').first()
    return render(request,
                  'data_management/index.html', {
                      'last_contest': last_contest,
                    });
                    
    return HttpResponse(question.question_text)

def load_contests(request):
    contests = Contest.objects.all()
    contest_ids = [c.id for c in contests]
    return render(request,
                  'data_management/load-contests.html', {
                        'contest_ids': contest_ids,
                      })
    return HttpResponse(', '.join([str(c.id) for c in contests]))

def save_contest(request):
    id = int(request.POST['id'])
    if id == -1:
        return HttpResponseRedirect(reverse('data:index'))
    
    name = request.POST['name']
    timestamp = int(request.POST['startTime'])
    date = datetime.datetime.fromtimestamp(timestamp)
    Contest.objects.create(id = id, name = name, date = date)
    return HttpResponseRedirect(reverse('data:load-contests'))

achievement_id_to_loader_name_mapping = {
        DID_NOT_SCRATCH_ME.id: 'did_not_scratch_me',
        PERESVET.id: 'peresvet',
    };

def update_achievement(request, achievementId):
    state = AchievementParseProgress_ByContest.get_for_achievement(achievementId)
    if state.lastParsedContest == None:
        minContestId = Contest.objects.all().aggregate(minId = Min('id'))['minId']
    else:
        minContestId = state.lastParsedContest.id + 1
    contest = Contest.objects.filter(id__gte = minContestId).order_by('id').first()
    if contest == None:
        return HttpResponseRedirect(reverse('data:index'))
    return render(request,
                  'data_management/load-achievement.html', {
                      'contestId': contest.id,
                      'achievementId': achievementId,
                      'loader_name': achievement_id_to_loader_name_mapping[int(achievementId)],
                })

def save_contest_achievement(request):
    contestId = int(request.POST['contestId'])
    contest = Contest.objects.get(pk = contestId)
    achievementId = int(request.POST['achievementId'])
    parseState = AchievementParseProgress_ByContest.get_for_achievement(achievementId)
    if parseState.lastParsedContest != None and parseState.lastParsedContest.id >= contest.id:
        return HttpResponse("Contest %d is already loaded for achievement id = %d" % (contestId, achievementId))
    achievements = json.loads(request.POST['resultData'])
    achievement = Achievement.objects.get(pk = achievementId)
    for data in achievements:
        handle = data['handle']
        comment = data['comment']

        contestant = Contestant.objects.get_or_create(handle = handle)[0]
        Rewarding.objects.create(participant = contestant, achievement = achievement, comment = comment, date = contest.date, contest = contest)
    parseState.lastParsedContest = contest
    parseState.save()
    return HttpResponseRedirect(reverse('data:update-achievement', args = [achievementId]))

def ratings_update(request):
    return render(request, 'data_management/update-ratings.html', None)

def ratings_save(request):
    data = json.loads(request.POST['resultData'])
    existing_handles = set()
    existing_handles.update([c.handle for c in Contestant.objects.all()])
    missing_ids = [c['handle'] for c in data if not (c['handle'] in existing_handles)]
    Contestant.objects.bulk_create([Contestant(handle = h) for h in missing_ids])
    
    temp_user_rating.objects.all().delete()
    temp_user_rating.objects.bulk_create([temp_user_rating(tmp_handle = h['handle'], tmp_rating = h['rating']) for h in data])
    
    cursor = connection.cursor()
    cursor.execute("update achievements_contestant set rating = (select tmp_rating from data_management_temp_user_rating where tmp_handle = handle)")
    temp_user_rating.objects.all().delete()
    return HttpResponseRedirect(reverse('data:index'))
  