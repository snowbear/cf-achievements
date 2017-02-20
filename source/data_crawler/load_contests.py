import pytz
from django.db.models import *

from data_crawler.cf_api import *
from data_crawler.cf_api_enums import *
from data_management.models import *


def add_contest(contest_id, name, timestamp):
    logging.info("Adding contest: %d - %d - %s", contest_id, timestamp, name)
    moscow_tz = pytz.timezone('Europe/Moscow')
    date = datetime.datetime.fromtimestamp(timestamp, pytz.utc).astimezone(moscow_tz)
    order = 1
    if Contest.objects.count() > 0:
        order = 1 + Contest.objects.all().aggregate(max_order=Max('order'))['max_order']
    
    utc_now = datetime.datetime.now(pytz.utc)

    Task.objects.create(name=Task.UPDATE_RATINGS, additional_id=contest_id, added_on=utc_now)
    Task.objects.create(name=Task.LOAD_DATA, additional_id=contest_id, added_on=utc_now)
    Task.objects.create(name=Task.UPDATE_ACHIEVEMENTS, additional_id=contest_id, added_on=utc_now)
    return Contest.objects.create(id=contest_id, name=name, date=date, order=order)


def load_contests(report):
    known_contests = {c.id for c in Contest.objects.all()}
    contests = sorted(get_contests(), key=lambda contest: contest['startTimeSeconds'])
    
    min_delay_before_adding_contest_in_seconds = 8 * 60 * 60
    min_timestamp = int(time()) - min_delay_before_adding_contest_in_seconds
    
    contests = [c for c in contests
                if c['id'] not in known_contests
                if contest_phase_mapping[c['phase']] == CONTEST_PHASE.FINISHED
                if c['startTimeSeconds'] + c['durationSeconds'] < min_timestamp
                ]

    for c in contests:
        added_contest = add_contest(c['id'], c['name'], c['startTimeSeconds'])
        report.add_line("Added contest <b>{name}</b> [{id}]", name=added_contest.name, id=added_contest.id)
