from django.db.models import *

from data_crawler.crawling_helpers import *
from data_management.models import *


def filter_hack(js):
    return is_cool_participant(js['hacker']) and \
           is_cool_participant(js['defender']) and \
           hack_verdict_mapping[js['verdict']] != HACK_VERDICT.OTHER


def to_hack(contest, problems, submissions, js):
    handle_hacker = js['hacker']['members'][0]['handle']
    handle_defender = js['defender']['members'][0]['handle']

    hacker = get_contestant_by_handle(handle_hacker)
    defender = get_contestant_by_handle(handle_defender)

    problem = problems[js['problem']['index']]

    creation_time_seconds = js['creationTimeSeconds']

    key = (defender, problem)
    matching_submissions = [s for s in submissions.get(key, []) if s.creation_time_seconds < creation_time_seconds]

    challenged_submission = (matching_submissions[0] if len(matching_submissions) > 0 else None)

    is_manual = js['judgeProtocol']['manual'] if 'judgeProtocol' in js else False

    return Hack(
            hacker=hacker,
            defender=defender,
            problem=problem,
            challenged_submission=challenged_submission,
            creation_time_seconds=creation_time_seconds,
            verdict=hack_verdict_mapping[js['verdict']],
            test_size=len(js['test']) if 'test' in js else None,
            is_manual=is_manual,
    )


def load_hacks(contest, report):
    existing_hacks_count = Hack.objects.filter(problem__contest=contest).count()
    assert (existing_hacks_count == 0)

    js = get_hacks(contest)

    problems = dict((p.index, p) for p in Problem.objects.filter(contest=contest))
    submission_query = Q(verdict=SUBMISSION_VERDICT.CHALLENGED) | Q(verdict=SUBMISSION_VERDICT.SKIPPED) | ~Q(
        testset=SUBMISSION_TESTSET.PRETESTS)
    submissions = Submission.objects.filter(submission_query, contest=contest).prefetch_related(Prefetch('author'),
                                                                                                Prefetch('problem'))

    grouped_submissions = dict()
    for sub in submissions:
        key = (sub.author, sub.problem)
        if key not in grouped_submissions:
            grouped_submissions[key] = []
        grouped_submissions[key].append(sub)

    for lst in grouped_submissions.values():
        lst.sort(key=lambda s: s.creation_time_seconds, reverse=True)
    hacks = [to_hack(contest, problems, grouped_submissions, h) for h in js if filter_hack(h)]
    Hack.objects.bulk_create(hacks)
    report.add_line("Hack: {n} added", n=len(hacks))
