import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from achievements.models import Contest

def index(request):
    last_contest = Contest.objects.order_by('-date').first()
    return render(request,
                  'data_management/index.html', {
                      'last_contest': last_contest,
                    });
                    
    return HttpResponse(question.question_text)

def load_contests(request):
    contests = Contest.objects.all()
    contest_ids = [c.cfId for c in contests]
    return render(request,
                  'data_management/load-contests.html', {
                        'contest_ids': contest_ids,
                      })
    return HttpResponse(', '.join([str(c.cfId) for c in contests]))

def save_contest(request):
    cfId = int(request.POST['id'])
    if cfId == -1:
        return HttpResponseRedirect(reverse('data:index'))
    
    name = request.POST['name']
    timestamp = int(request.POST['startTime'])
    date = datetime.datetime.fromtimestamp(timestamp)
    new_contest = Contest(cfId = cfId, name = name, date = date)
    new_contest.save()
    return HttpResponseRedirect(reverse('data:load-contests'))
