import datetime, django, json, logging, logging.config, os, sys
import http.client
from collections import defaultdict
from pytz import timezone
from django.db.models import *

from achievements.models import *
from data_management.models import *

from cf_api import *
from cf_api_enums import *
from crawling_helpers import *

def filter_submission(js):
    return is_cool_participant(js['author'])

def to_submission(contest, problems, js):
    handle = get_main_handle(js['author'])
    author = get_contestant_by_handle(handle)   
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
    logging.info("Adding %d submissions", len(submissions))
    Submission.objects.bulk_create(submissions)
