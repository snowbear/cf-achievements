import datetime, django, json, logging, logging.config, os, sys
import http.client
from itertools import *
from collections import defaultdict
from pytz import timezone
from django.db.models import *
from django.db import *

from cf_api import *

def user_tag(handle):
	return "[user:%s]" % handle

def contest_tag(contest):
	return "[contest:%d]" % contest.id

def join_with_commas_and_and(items):
    items = list(items)
    result = ""
    last_index = len(items) - 1
    for i,item in zip(range(len(items)), items):
        if i != 0 and i == last_index: result = result + " and "
        elif i > 0: result = result + ", "
        result += item;
    
    return result;
    
    
def add_achievement(list, achievement, contest, contestant, comment, level = None):
    rewarding = Rewarding(participant = contestant, achievement = achievement, comment = comment, date = contest.date, contest = contest, level = level)
    list.append(rewarding)

def execute_sql(sql):
    logging.debug("Executing SQL:")
    logging.debug(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor

def batch_insert(table_name, column_names, values_list):
    assert(type(column_names) == tuple)
    if len(values_list) == 0: return
    
    values_string = ",".join(str(val) for val in values_list)
    query = '''
            INSERT INTO %s (%s)
            VALUES
            %s
            ''' % (table_name , ",".join(column_names) , values_string)
    execute_sql(query)
    
class achievement_parser:
    def __init__(self, parser):
        self.parser = parser

class language_expert_achievement_parser:
    def __init__(self, language_group, language_string):
        self.language_group = language_group
        self.language_string = language_string
        
    def parser(self, achievement, contest):
        current_result = execute_sql('''
                SELECT count(*) FROM data_management_achievement_contestant_progress_by_contest
                WHERE
                    achievement_id = %d AND
                    contest_id = %d
            ''' % (achievement.id , contest.id)).fetchone()[0]
                
        assert(current_result == 0)
    
        official_contestants = Contestant.objects.filter(contestparticipation__contest = contest, contestparticipation__participant_type = PARTICIPANT_TYPE.CONTESTANT)
        matching_languages = [ l.value for l in all_languages if l.group == self.language_group ]
        assert(len(matching_languages) > 0)
        submissions = list(Submission.objects.filter(contest = contest, 
                                                     verdict = SUBMISSION_VERDICT.OK, 
                                                     author__in = official_contestants,
                                                     language__in = matching_languages)
                                                .values('author')
                                                .annotate(problems = Count('problem', distinct = True)) 
                            )
                                                     
        batch_insert(
                    'data_management_achievement_contestant_progress_by_contest',
                    ('achievement_id' , 'contestant_id' , 'contest_id' , 'progress'),
                    [ (achievement.id , row['author'] , contest.id , row['problems']) for row in submissions ],
                    )
                    
        new_achievements = execute_sql('''
                SELECT contestant_id
                FROM data_management_achievement_contestant_progress_by_contest
                WHERE achievement_id = %d
                    AND contestant_id NOT IN (SELECT DISTINCT participant_id FROM achievements_rewarding WHERE achievement_id = %d)
                GROUP BY contestant_id
                HAVING SUM(progress) >= %d
            ''' % (achievement.id , achievement.id , problems_for_language_achievement))
        
        return [ Rewarding(
                            participant = Contestant(id = row[0]),
                            achievement = achievement,
                            comment = get_award_comment(self.language_string),
                            contest = contest,
                            date = contest.date,
                            ) for row in new_achievements ]
        
def get_achievements_did_not_scratch_me(achievement, contest):
    tourist = Contestant.objects.get(handle = 'tourist')
    his_hacks = Hack.objects.filter(problem__contest = contest, hacker = tourist)
    was_hacked = set((h.defender , h.problem) for h in his_hacks if h.verdict == HACK_VERDICT.HACK_SUCCESSFUL)
    was_not_hacked = set((h.defender , h.problem) for h in his_hacks if h.verdict == HACK_VERDICT.HACK_UNSUCCESSFUL)
    result = was_not_hacked - was_hacked
    res_list = list()
    for reward in result:
        problem = reward[1]
        comment = "the successful defence of his problem %s from %s during %s" % (problem , user_tag(tourist.handle) , contest_tag(contest))
        add_achievement(res_list, achievement, contest, reward[0], comment)
    return res_list

def get_achievements_peresvet(achievement, contest):
    hacks = [ h for h in Hack.objects.filter(problem__contest = contest) \
                        if h.verdict == HACK_VERDICT.HACK_SUCCESSFUL \
            ]
    
    submissions = Submission.objects.filter(contest = contest).values('author', 'problem__index').annotate(last_submission = Max('creation_time_seconds'))
    last_submissions = dict([ ((s['author'] , s['problem__index']) , s['last_submission']) for s in submissions ])
            
    mutual_hacks = [ ( (x.hacker , x.defender , x.problem) , min(x.creation_time_seconds , y.creation_time_seconds))
                                for x in hacks for y in hacks
                                                if x.hacker.handle < x.defender.handle \
                                                if x.hacker == y.defender \
                                                if x.defender == y.hacker \
                                                if x.problem == y.problem \
             ]

    last_mutual_hack = list((k, min(x[1] for x in g)) for (k,g) in groupby(mutual_hacks, lambda x : x[0]))
    res_list = list()
    achievement_giver = lambda h1, h2, p : \
                add_achievement(res_list, achievement, contest, h1, "the successful mutual hack with %s on problem %s in %s" % (user_tag(h2) , p.index , contest_tag(contest)));

    for (key,t) in last_mutual_hack:
        h1 = key[0]
        h2 = key[1]
        problem = key[2]
        if t > max(last_submissions[(h1.id , problem.index)] , last_submissions[(h2.id , problem.index)]):
            achievement_giver(h1, h2, problem)
            achievement_giver(h2, h1, problem)
    return res_list

def get_achievements_polyglot(achievement, contest):
    submissions =  list(Submission.objects.raw('''
            SELECT sub.*
            FROM data_management_submission sub
            JOIN data_management_contestParticipation part ON part.contest_id = sub.contest_id AND part.contestant_id = sub.author_id
            WHERE
                sub.contest_id = %s
                AND part.participant_type = %s
                AND sub.verdict = %s
                AND sub.language <> %s
            ORDER BY sub.author_id
        ''', 
        [ contest.id , PARTICIPANT_TYPE.CONTESTANT.value , SUBMISSION_VERDICT.OK.value , Languages.SecretLanguage.value ]))
        
    grouped_submissions = groupby(submissions, lambda s : s.author)
    
    res = []
    for contestant, subs in grouped_submissions:
        languages = set(language_mapping(s.language) for s in subs)
        language_groups = set(l.group for l in languages)
        if len(language_groups) > 1:
            languages_string = join_with_commas_and_and([ l.name for l in languages ])
            add_achievement(res, achievement, contest, contestant, "the usage of %s to solve problems in %s" % (languages_string, contest_tag(contest)), len(language_groups) - 1)
            
    return res

def get_achievements_language_does_not_matter(achievement, contest):
    ulr_round_ids = { 64 , 72 , 100 , 130 , 153 , 162 , 188 , 345 , 470 }
    if contest.id not in ulr_round_ids: return []

    submissions = list(Submission.objects.filter(contest = contest, verdict = SUBMISSION_VERDICT.OK).all().order_by('author__id'))
    
    res_list = []
    
    for contestant, subs in groupby(submissions, lambda s : s.author):
        solved_problems = set(s.problem for s in subs)
        
        if len(solved_problems) < 2: continue
        problems_string = join_with_commas_and_and(sorted([ p.index for p in solved_problems ]))
        add_achievement(res_list, achievement, contest, contestant, "the problems %s solved during %s" % (problems_string ,contest_tag(contest)))
    return res_list

def get_achievements_speck_in_your_brothers_eye(achievement, contest):
    verdict_query = Q(verdict__in = [
                                    SUBMISSION_VERDICT.FAILED ,
                                    SUBMISSION_VERDICT.RUNTIME_ERROR ,
                                    SUBMISSION_VERDICT.WRONG_ANSWER ,
                                    SUBMISSION_VERDICT.PRESENTATION_ERROR ,
                                    SUBMISSION_VERDICT.TIME_LIMIT_EXCEEDED ,
                                    SUBMISSION_VERDICT.MEMORY_LIMIT_EXCEEDED ,
                                    SUBMISSION_VERDICT.IDLENESS_LIMIT_EXCEEDED ,
                                    SUBMISSION_VERDICT.CRASHED ,
                                    ])
    tests_query = ~Q(testset__in = [ SUBMISSION_TESTSET.SAMPLES , SUBMISSION_TESTSET.PRETESTS , SUBMISSION_TESTSET.CHALLENGES ])
    submissions = list(Submission.objects.filter(tests_query, verdict_query, contest = contest).prefetch_related(Prefetch('author'), Prefetch('problem')).all())
    bad_solvers = set((s.author, s.problem) for s in submissions)
    
    hacks = Hack.objects.filter(problem__contest = contest, verdict = HACK_VERDICT.HACK_SUCCESSFUL).prefetch_related(Prefetch('hacker'), Prefetch('problem'))
    successful_hackers = set((h.hacker , h.problem) for h in hacks)
    
    return [ Rewarding( participant = author,
                        achievement = achievement,
                        comment = "successful challenge on problem %s during %s while his/her own code was not perfect either" % ( problem.index , contest_tag(contest)),
                        contest = contest,
                        date = contest.date)
                    for author,problem in successful_hackers & bad_solvers
            ]
            
def get_achievements(achievement, contest):
    parser = achievement_parsers[achievement.id]
    rewardings = parser.parser(achievement, contest)
    for a in rewardings:
        logging.info("Got an achievement '%s'. Handle: %s. Comment: %s. level: %s", achievement.name, a.participant.handle, a.comment, str(a.level));

    Rewarding.objects.bulk_create(rewardings)

# logging.basicConfig(filename=__file__ + ".log", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logging.config.fileConfig('logging.conf', disable_existing_loggers = False)

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir , "../"))
django.setup()

from achievements.models import *
from achievements.achievement_data import *
from data_management.models import *

achievement_parsers = {
                        DID_NOT_SCRATCH_ME.id : achievement_parser(get_achievements_did_not_scratch_me),
                        PERESVET.id : achievement_parser(get_achievements_peresvet),
                        POLYGLOT.id : achievement_parser(get_achievements_polyglot),
                        LANGUAGE_DOES_NOT_MATTER.id : achievement_parser(get_achievements_language_does_not_matter),
                        SPECK_IN_YOUR_BROTHERS_EYE.id: achievement_parser(get_achievements_speck_in_your_brothers_eye),
                        LANGUAGE_ACHIEVEMENT_C.id: language_expert_achievement_parser(LANGUAGE_GROUP.C , "C"),
                        LANGUAGE_ACHIEVEMENT_CPP.id: language_expert_achievement_parser(LANGUAGE_GROUP.Cpp , "C++"),
                        LANGUAGE_ACHIEVEMENT_CS.id: language_expert_achievement_parser(LANGUAGE_GROUP.CSharp , "C#"),
                        LANGUAGE_ACHIEVEMENT_D.id: language_expert_achievement_parser(LANGUAGE_GROUP.D , "D"),
                        LANGUAGE_ACHIEVEMENT_GO.id: language_expert_achievement_parser(LANGUAGE_GROUP.Go , "Go"),
                        LANGUAGE_ACHIEVEMENT_HASKELL.id: language_expert_achievement_parser(LANGUAGE_GROUP.Haskell , "Haskell"),
                        LANGUAGE_ACHIEVEMENT_JAVA.id: language_expert_achievement_parser(LANGUAGE_GROUP.Java , "Java"),
                        LANGUAGE_ACHIEVEMENT_OCAML.id: language_expert_achievement_parser(LANGUAGE_GROUP.Ocaml , "OCaml"),
                        LANGUAGE_ACHIEVEMENT_PASCAL.id: language_expert_achievement_parser(LANGUAGE_GROUP.Pascal , "Pascal"),
                        LANGUAGE_ACHIEVEMENT_PERL.id: language_expert_achievement_parser(LANGUAGE_GROUP.Perl , "Perl"),
                        LANGUAGE_ACHIEVEMENT_PHP.id: language_expert_achievement_parser(LANGUAGE_GROUP.PHP , "PHP"),
                        LANGUAGE_ACHIEVEMENT_PYTHON.id: language_expert_achievement_parser(LANGUAGE_GROUP.Python , "Python"),
                        LANGUAGE_ACHIEVEMENT_RUBY.id: language_expert_achievement_parser(LANGUAGE_GROUP.Ruby , "Ruby"),
                        LANGUAGE_ACHIEVEMENT_SCALA.id: language_expert_achievement_parser(LANGUAGE_GROUP.Scala , "Scala"),
                        LANGUAGE_ACHIEVEMENT_JAVASCRIPT.id: language_expert_achievement_parser(LANGUAGE_GROUP.JavaScript , "JavaScript"),
                      }

if __name__ == '__main__':                      
    last_contest = Contest.objects.order_by('-order').first()

    for achievement in Achievement.objects.all():
        # if achievement.id != 101: continue

        logging.info("Checking achievement '%s'...", achievement.name)
        
        last_parse_order = -1
        state = AchievementParseProgress_ByContest.get_for_achievement(achievement.id)
        if state.lastParsedContest != None:
            last_parse_order = state.lastParsedContest.order
        
        while last_parse_order < last_contest.order:
            contest = Contest.objects.filter(order__gt = last_parse_order).order_by('order').first()
            logging.info("Next contest to update: %s (id = %d)", contest.name, contest.id)
            get_achievements(achievement, contest)
            last_parse_order = contest.order
            state.lastParsedContest = contest
            state.save()
        logging.info("Done checking achievement '%s'", achievement.name)
