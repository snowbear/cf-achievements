from django.db.models import *
from cf_api import *

from helpers.sql import *
from achievements.models import *
from data_management.models import *

def update_ratings(report):
    js = get_ratings()
    data = [ (j['handle'] , j['rating']) for j in js ]
    existing_handles = set( c.handle for c in Contestant.objects.all() )
    missing_handles = [ c[0] for c in data if not (c[0] in existing_handles) ]
    Contestant.objects.bulk_create([Contestant(handle = h) for h in missing_handles])
    
    updated_user_count = batch_update("achievements_contestant", "handle", "rating", data )
    report.add_line("Rating updated, {n} users affected".format(n = updated_user_count))

def update_ratings_dispatcher_task(task, report):
    if Task.objects.filter(name = Task.UPDATE_RATINGS, id__gt = task.id, finished_on__isnull = True).count() > 0:
        report.add_line("Task avoided since there is another similar task in queue")
        return
    update_ratings(report)