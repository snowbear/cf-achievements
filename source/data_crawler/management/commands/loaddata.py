import datetime
import logging
import pytz
from django.core.mail import *
from django.core.management.base import BaseCommand

from achievements.models import *

from data_crawler.load_contest_participations import load_contest_participations
from data_crawler.load_contests import load_contests
from data_crawler.load_hacks import load_hacks
from data_crawler.load_problems import load_problems
from data_crawler.load_submissions import load_submissions
from data_crawler.ReportBuilder import ReportBuilder
from data_crawler.update_achievement import update_achievements
from data_crawler.update_ratings import update_ratings_dispatcher_task
from data_management.models import Task


def load_data(task, report):
    contest = Contest.objects.get(pk=task.additional_id)
    report.add_line("Loading data for contest <b>{name}</b>", name=contest.name)
    load_contest_participations(contest, report)
    load_problems(contest, report)
    load_submissions(contest, report)
    load_hacks(contest, report)


def get_remaining_tasks_query():
    return Task.objects.filter(finished_on__isnull=True)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.config.fileConfig('data_crawler/logging.conf')

        report = ReportBuilder()
        load_contests(report)
        print("Hello")
        print(report.get_result())

        if get_remaining_tasks_query().count() > 0:
            logging.info("{n} tasks to go".format(n=get_remaining_tasks_query().count()))

            try:
                while get_remaining_tasks_query().count() > 0:
                    first_task = get_remaining_tasks_query().order_by("id")[0]
                    report.add_line("Task to cover: {name}, added on: {added_on}, additional_id: {additional_id}",
                                    name=first_task.name, added_on=first_task.added_on,
                                    additional_id=first_task.additional_id)
                    if first_task.name == Task.UPDATE_RATINGS:
                        update_ratings_dispatcher_task(first_task, report)
                    elif first_task.name == Task.LOAD_DATA:
                        load_data(first_task, report)
                    elif first_task.name == Task.UPDATE_ACHIEVEMENTS:
                        update_achievements(first_task, report)
                    else:
                        raise Exception("Unexpected task_name = " + first_task.name)

                    first_task.finished_on = datetime.datetime.now(pytz.utc)
                    first_task.save()

                mail_managers('Dispatcher finished its job', report.get_result(), html_message=report.get_html_result())
            except Exception as e:
                report.add_error(e)
                mail_admins('Dispatcher job failed', report.get_result(), html_message=report.get_html_result())
            logging.info("Done")
