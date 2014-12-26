import datetime
import json

from django.db import connection
from django.db.models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from achievements.models import *
from achievements.achievement_data import *
from data_management.models import *

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
    order = 1
    if Contest.objects.count() > 0:
        order = 1 + Contest.objects.all().aggregate(max_order = Max('order'))['max_order']
    Contest.objects.create(id = id, name = name, date = date, order = order)
    return HttpResponseRedirect(reverse('data:load-contests'))

achievement_id_to_loader_name_mapping = {
        DID_NOT_SCRATCH_ME.id: 'did_not_scratch_me',
        PERESVET.id: 'peresvet',
        POLYGLOT.id: 'polyglot',
        LANGUAGE_DOES_NOT_MATTER.id: 'language_does_not_matter',
    };

def update_achievement(request, achievementId):
    state = AchievementParseProgress_ByContest.get_for_achievement(achievementId)
    if state.lastParsedContest == None:
        minContestOrder = Contest.objects.all().aggregate(minOrder = Min('order'))['minOrder']
    else:
        minContestOrder = state.lastParsedContest.order + 1
    contest = Contest.objects.filter(order__gte = minContestOrder).order_by('order').first()
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
    if parseState.lastParsedContest != None and parseState.lastParsedContest.order >= contest.order:
        return HttpResponse("Contest %d is already loaded for achievement id = %d" % (contestId, achievementId))
    achievements = json.loads(request.POST['resultData'])
    achievement = Achievement.objects.get(pk = achievementId)
    for data in achievements:
        handle = data['handle']
        comment = data['comment']
        level = None
        if 'level' in data:
            level = data['level']

        contestant = Contestant.objects.get_or_create(handle = handle)[0]
        Rewarding.objects.create(participant = contestant, achievement = achievement, comment = comment, date = contest.date, contest = contest, level = level)
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

    query = """
    UPDATE achievements_contestant as c
    SET rating = s.rating
    FROM (
        SELECT * 
        FROM ( VALUES 
        """ + ",".join(["('%s',%d)" % (h['handle'], h['rating']) for h in data]) + """
        ) AS x(handle, rating)
    )s
    where c.handle = s.handle
    """
    cursor = connection.cursor()
    cursor.execute(query)
    
    return HttpResponseRedirect(reverse('data:index'))
