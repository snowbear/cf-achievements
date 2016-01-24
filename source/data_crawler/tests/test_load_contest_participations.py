from django import test

from achievements import models
from data_crawler.ReportBuilder import ReportBuilder
from data_crawler.load_contest_participations import load_contest_participations


class Tests(test.TestCase):
    def test_contest_with_duplicate_participations(self):
        contest = models.Contest(id=158)  # "VK Cup 2012 Qualification Round 1" contains 2 duplicate participants
        report = ReportBuilder()

        load_contest_participations(contest, report)
