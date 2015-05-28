from colorama import init, Fore
init()

import sys, os, django, logging, logging.config
logging.config.fileConfig('logging.conf', disable_existing_loggers = False)
current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(current_dir , "../", "source"))

django.setup()


from achievements.models import *
from helpers.sql import *

latest_contest = Contest.objects.all().order_by("-order")[0]
print("You are going to rollback contest: " + Fore.RED + latest_contest.name + Fore.RESET + ", id = " + str(latest_contest.id))

sys.stdout.write("Type 'yes' to continue: ")
response = input()

if response == "yes":
    prev_contest = Contest.objects.filter(order__lt = latest_contest.order).order_by("-order")[0]
    logging.info("Rolling back...")
    logging.info("Prev contest = {name}, id = {id}".format(name = prev_contest.name, id = prev_contest.id))
    execute_sql("DELETE FROM data_management_task WHERE additional_id = {id};".format(id = latest_contest.id))
    execute_sql("DELETE FROM achievements_rewarding WHERE contest_id = {id};".format(id = latest_contest.id))
    execute_sql("DELETE FROM data_management_achievement_contestant_progress_by_contest WHERE contest_id = {id};".format(id = latest_contest.id))
    
    execute_sql("DELETE FROM data_management_hack WHERE problem_id IN (SELECT id from data_management_problem WHERE contest_id = {id});".format(id = latest_contest.id))
    execute_sql("DELETE FROM data_management_submission WHERE contest_id = {id};".format(id = latest_contest.id))
    execute_sql("DELETE FROM data_management_problem WHERE contest_id = {id};".format(id = latest_contest.id))
    execute_sql("DELETE FROM data_management_ContestParticipation WHERE contest_id = {id};".format(id = latest_contest.id))
    execute_sql("DELETE FROM achievements_contest WHERE id = {id};".format(id = latest_contest.id))
    logging.info("Done")
    
else:
    print("Cancelled")