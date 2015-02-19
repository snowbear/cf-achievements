import django, logging, logging.config, os, sys

logging.config.fileConfig('logging.conf')

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir , "../"))
django.setup()

from load_contests import *
from load_problems import *
from load_submissions import *
from load_hacks import *
from load_contest_participations import *
from achievements.models import *
from data_management.models import *

load_contests()

for c in Contest.objects.all():
    if ContestParticipation.objects.filter(contest = c).count() == 0:
        load_contest_participations(c)

    if c.problem_set.count() == 0:
        load_problems(c)
    
    if c.submission_set.count() == 0:
        load_submissions(c)
        
    if Hack.objects.filter(problem__contest = c).count() == 0:
        load_hacks(c)
    
logging.info("Done")