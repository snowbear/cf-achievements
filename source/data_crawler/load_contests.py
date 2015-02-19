import datetime, django, json, logging, logging.config, os, sys
import http.client
import pytz
from django.db.models import *

from cf_api import *
from cf_api_enums import *
from achievements.models import *
    
def add_contest(id, name, timestamp):
    logging.info("Adding contest: %d - %d - %s" , id , timestamp , name)
    moscow_tz = pytz.timezone('Europe/Moscow')
    date = datetime.datetime.fromtimestamp(timestamp, pytz.utc).astimezone(moscow_tz)
    order = 1
    if Contest.objects.count() > 0:
        order = 1 + Contest.objects.all().aggregate(max_order = Max('order'))['max_order']
    Contest.objects.create(id = id, name = name, date = date, order = order)

def load_contests():
    known_contests = { c.id for c in Contest.objects.all() }
    contests = sorted(get_contests(), key = lambda contest: contest['startTimeSeconds'])
    contests = [ c for c in contests \
                            if c['id'] not in known_contests \
                            if contest_phase_mapping[c['phase']] == CONTEST_PHASE.FINISHED \
                ]
    for c in contests:
        add_contest(c['id'], c['name'], c['startTimeSeconds'])