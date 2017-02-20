import logging
from os import path
from django.core.management.base import BaseCommand

from achievements import models
from helpers import sql


class Command(BaseCommand):
    args = 'contest_id'
    help = 'Removes all the data loaded for a particular contest. Has no effect on calculated data like rewardings.'

    def handle(self, *args, **options):
        logging_config_path = path.join(path.dirname(__file__), path.pardir, path.pardir, 'logging.conf')
        logging.config.fileConfig(logging_config_path)

        contest_id = args[0]
        contest = models.Contest.objects.get(pk=contest_id)

        logging.info("Removing data for contest {name}".format(name=contest))

        sql.execute_sql("DELETE FROM data_management_hack "
                        "WHERE problem_id IN ("
                        "SELECT id from data_management_problem WHERE contest_id = {id});"
                        .format(id=contest.id))

        sql.execute_sql("DELETE FROM data_management_submission "
                        "WHERE contest_id = {id};".format(id=contest.id))

        sql.execute_sql("DELETE FROM data_management_problem WHERE contest_id = {id};".format(id=contest.id))

        sql.execute_sql("DELETE FROM data_management_ContestParticipation "
                        "WHERE contest_id = {id};".format(id=contest.id))
