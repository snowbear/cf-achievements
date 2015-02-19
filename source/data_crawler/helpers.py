from cf_api import *
from cf_api_enums import *

from achievements.models import *

def is_online_participant(js):
    participant_type = participant_type_mapping[js['participantType']]
    return participant_type == PARTICIPANT_TYPE.CONTESTANT or participant_type == PARTICIPANT_TYPE.OUT_OF_COMPETITION

def is_cool_participant(js):
    return not js['ghost'] and len(js['members']) == 1 and is_online_participant(js)
    
def get_main_handle(js_party):
    return js_party['members'][0]['handle']
    
class HELPERS_STATIC:
    to_contestant_map = { }
    
def get_contestant_by_handle(handle):
    if len(HELPERS_STATIC.to_contestant_map) == 0:
        HELPERS_STATIC.to_contestant_map = dict( (c.handle , c) for c in Contestant.objects.all() )
    if not handle in HELPERS_STATIC.to_contestant_map:
        contestant = Contestant.objects.get_or_create(handle = handle)[0]
        HELPERS_STATIC.to_contestant_map[handle] = contestant
    return HELPERS_STATIC.to_contestant_map[handle]
    