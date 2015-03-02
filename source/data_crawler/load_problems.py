from django.db.models import *
from cf_api import *

from achievements.models import *
from data_management.models import *

def to_problem(contest, order, js):
    return Problem(
                contest = contest,
                index = js['index'],
                order = order,
                name = js['name'],
                points = js.get('points'),
            )

def load_problems(contest):
    existing_problems_count = Problem.objects.filter(contest = contest).count()
    assert(existing_problems_count == 0)
    
    js = get_problems(contest)
    
    problems = [ to_problem(contest, i, p) for (i,p) in zip(range(len(js)),js) ]
    Problem.objects.bulk_create(problems)