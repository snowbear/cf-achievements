from django.db.models import *
from cf_api import *

from achievements.models import *
from data_management.models import *
from crawling_helpers import *

class multi_user_hack:
    def __init__(self, users):
        self.all_bogus_handles = users
        self.users_to_skip = set()
        
    def check_user(self, handle):
        if handle not in self.all_bogus_handles: return True
        should_be_skipped = handle in self.users_to_skip
        print("adding handle" , handle, should_be_skipped)
        self.users_to_skip.add(handle)
        return not should_be_skipped

class hack_for_multi_handles:
    hacks = {
                158: multi_user_hack( { 'palmerstone' , 'r_hero' } ),
                172: multi_user_hack( { 'pepela' } ),
                447: multi_user_hack( { 'MehrdadAP' , 'kasim' } ),
                472: multi_user_hack( { 'yagfair' , 'a00920' } ),
                493: multi_user_hack( { 'lstaresinic' } ),
            }

def filter_participant(js_ranking):
    if not is_cool_participant(js_ranking['party']): return False
    handle = get_main_handle(js_ranking['party'])
    
    if js_ranking['party']['contestId'] in hack_for_multi_handles.hacks:
        hack = hack_for_multi_handles.hacks[js_ranking['party']['contestId']]
        if not hack.check_user(handle): return False
    return True

def to_contest_participation(contest, js):
    handle = get_main_handle(js['party'])
    return ContestParticipation(
                contest = contest,
                contestant = get_contestant_by_handle(handle),
                participant_type = participant_type_mapping[js['party']['participantType']],
                taken_place = js.get('rank'),
                successful_hacks = js['successfulHackCount'],
                unsuccessful_hacks = js['unsuccessfulHackCount'],
                room = js['party'].get('room'),
            )

def load_contest_participations(contest, report):
    existing_contest_participations_count = ContestParticipation.objects.filter(contest = contest).count()
    assert(existing_contest_participations_count == 0)
    
    js = get_contest_participants(contest)
    js = [ j for j in js if filter_participant(j) ]
    
    contest_participations = [ to_contest_participation(contest, p) for p in js ]
    ContestParticipation.objects.bulk_create(contest_participations)
    report.add_line("ContestParticipation: {n} added", n = len(contest_participations))