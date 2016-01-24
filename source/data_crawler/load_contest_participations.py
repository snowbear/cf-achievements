from more_itertools.recipes import unique_justseen

from data_crawler.crawling_helpers import *
from data_management.models import *


def filter_participant(js_ranking):
    if not is_cool_participant(js_ranking['party']):
        return False

    return True


def to_contest_participation(contest, js):
    handle = get_main_handle(js['party'])
    return ContestParticipation(
            contest=contest,
            contestant=get_contestant_by_handle(handle),
            participant_type=participant_type_mapping[js['party']['participantType']],
            taken_place=js.get('rank'),
            successful_hacks=js['successfulHackCount'],
            unsuccessful_hacks=js['unsuccessfulHackCount'],
            room=js['party'].get('room'),
    )


def load_contest_participations(contest, report):
    existing_contest_participations_count = ContestParticipation.objects.filter(contest=contest).count()
    assert (existing_contest_participations_count == 0)

    js = get_contest_participants(contest)
    js = [j for j in js if filter_participant(j)]

    contest_participations = [to_contest_participation(contest, p) for p in js]
    contest_participations.sort(key=lambda p: (p.contestant.id, p.taken_place))
    contest_participations = list(unique_justseen(contest_participations, lambda p: p.contestant.id))

    ContestParticipation.objects.bulk_create(contest_participations)
    report.add_line("ContestParticipation: {n} added", n=len(contest_participations))
