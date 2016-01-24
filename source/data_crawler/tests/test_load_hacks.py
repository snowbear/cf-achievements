from django import test

from achievements import models
from data_management.models import Problem
from data_crawler.ReportBuilder import ReportBuilder
from data_crawler.load_hacks import load_hacks


class Tests(test.TestCase):
    def test_loading_hacks_with_no_judge_protocol(self):
        contest = models.Contest(id=21)
        report = ReportBuilder()

        for problem_index in range(ord('A'), ord('E') + 1):
            Problem.objects.create(contest=contest,
                                   index=chr(problem_index),
                                   order=problem_index,
                                   name='problem',
                                   )
        load_hacks(contest, report)
