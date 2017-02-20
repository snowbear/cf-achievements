from data_crawler import cf_api

from achievements.models import *
from helpers import sql


def update_ratings_dispatcher_task(task, report):
    contest = Contest.objects.get(pk=task.additional_id)
    js = cf_api.get_rating_changes(contest)
    data = [(j['handle'], j['newRating']) for j in js]
    existing_handles = set(c.handle for c in Contestant.objects.all())
    missing_handles = [c[0] for c in data if c[0] not in existing_handles]
    Contestant.objects.bulk_create([Contestant(handle=h) for h in missing_handles])

    updated_user_count = sql.batch_update("achievements_contestant", "handle", "rating", data)
    report.add_line("Rating updated, {n} users affected".format(n=updated_user_count))
