from colorama import init, Fore
init()

import sys, os, django, logging, logging.config
logging.config.fileConfig('logging.conf', disable_existing_loggers = False)
current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(current_dir , "../", "source"))

django.setup()


from achievements.models import *
from helpers.sql import *

sys.stdout.write("Enter achievement Id: ")
id = int(input())

achievement = Achievement.objects.get(pk = id)
print("You are going to rollback achievement: " + Fore.RED + achievement.name + Fore.RESET)

sys.stdout.write("Type 'yes' to continue: ")
response = input()

if response == "yes":
    logging.info("Rolling back...")
    execute_sql("DELETE FROM data_management_achievementparseprogress_bycontest WHERE achievement_id = {id};".format(id = achievement.id))
    execute_sql("DELETE FROM achievements_rewarding WHERE achievement_id = {id};".format(id = achievement.id))
    execute_sql("DELETE FROM data_management_achievement_contestant_progress WHERE achievement_id = {id};".format(id = achievement.id))
    execute_sql("DELETE FROM data_management_achievement_contestant_progress_by_contest WHERE achievement_id = {id};".format(id = achievement.id))
    logging.info("Done")
    
else:
    print("Cancelled")