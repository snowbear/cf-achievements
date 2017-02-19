import logging
from os import path
from django.core.management.base import BaseCommand

from helpers import sql
from data_management.models import *


class Command(BaseCommand):
    help = 'Removes all data from the database. Happy New Year!'

    def handle(self, *args, **options):
        logging_config_path = path.join(path.dirname(__file__), path.pardir, path.pardir, 'logging.conf')
        logging.config.fileConfig(logging_config_path)

        logging.info("Prepare to say good bye to everything")

        sql.clear_table('data_management_achievement_contestant_progress_by_contest')

        sql.clear_table('data_management_hack')
        sql.clear_table('data_management_submission')
        sql.clear_table('data_management_problem')
        sql.clear_table('data_management_contestparticipation')
        sql.clear_table('data_management_AchievementParseProgress_ByContest')
        sql.clear_table('data_management_Task')

        sql.clear_table('achievements_Rewarding')
        sql.clear_table('achievements_Contest')
        sql.clear_table('achievements_Contestant')

        logging.info("Done")
