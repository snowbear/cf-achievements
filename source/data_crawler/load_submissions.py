import datetime, django, json, logging, logging.config, os, sys
import http.client
from collections import defaultdict
from pytz import timezone
from django.db.models import *

from achievements.models import *
from data_management.models import *

from cf_api import *
from cf_api_enums import *

def filter_submission(js):
    pt = participant_type_mapping[js['author']['participantType']]
    return \
        len(js['author']['members']) == 1 and \
        not js['author']['ghost'] and \
        (pt == PARTICIPANT_TYPE.CONTESTANT or pt == PARTICIPANT_TYPE.OUT_OF_COMPETITION)

class STATIC:        
    to_contestant_id_map = { }
    
def to_contestant_id(handle):
    if len(STATIC.to_contestant_id_map) == 0:
        STATIC.to_contestant_id_map = dict( (c.handle , c) for c in Contestant.objects.all() )
    if not handle in STATIC.to_contestant_id_map:
        contestant = Contestant.objects.get_or_create(handle = handle)[0]
        STATIC.to_contestant_id_map[handle] = contestant
    return STATIC.to_contestant_id_map[handle]

def to_submission(contest, problems, js):
    handle = js['author']['members'][0]['handle']
    author = to_contestant_id(handle)   
    return Submission(
                id = js['id'],
                contest = contest,
                creation_time_seconds = js['creationTimeSeconds'],
                relative_time_seconds = js['relativeTimeSeconds'],
                problem = next(p for p in problems if p.index == js['problem']['index']),
                author = author,
                language = language_mapping(js['programmingLanguage']).value,
                verdict = submission_verdict_mapping[js['verdict']],
                testset = submission_testset_mapping[js['testset']],
                passed_test_count = js['passedTestCount'],
                time_consumed_milliseconds = js['timeConsumedMillis'],
                memory_consumed_bytes = js['memoryConsumedBytes'],
            )

def load_submissions(contest):
    existing_submissions_count = Submission.objects.filter(contest = contest).count()
    assert(existing_submissions_count == 0)

    js = get_submissions(contest)

    problems = Problem.objects.filter(contest = contest)
    submissions = [ to_submission(contest, problems, s) for s in js if filter_submission(s) ]
    Submission.objects.bulk_create(submissions)
