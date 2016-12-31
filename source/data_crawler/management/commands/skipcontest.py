import datetime
import logging
import pytz
from os import path
from django.core.management.base import BaseCommand

from achievements import models
from data_management.models import Task


class Command(BaseCommand):
    args = 'contest_id'
    help = 'Marks remaining tasks for the given contest as finished'

    def handle(self, *args, **options):
        logging_config_path = path.join(path.dirname(__file__), path.pardir, path.pardir, 'logging.conf')
        logging.config.fileConfig(logging_config_path)

        contest_id = args[0]
        contest = models.Contest.objects.get(pk=contest_id)

        logging.info("Finishing remaining tasks for contest {name}".format(name=contest))

        contest_tasks = Task.objects.filter(finished_on__isnull=True, additional_id=contest.id)
        contest_tasks.update(finished_on=datetime.datetime.now(pytz.utc))
