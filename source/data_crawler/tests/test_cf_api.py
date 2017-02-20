from django import test

from achievements import models
from data_crawler import cf_api


class Tests(test.TestCase):
    def test_get_rating_changes_returns_correct_number_of_rows(self):
        contest = models.Contest(id=1)

        data = cf_api.get_rating_changes(contest)
        self.assertEqual(66, len(data))

    def test_get_rating_changes_returns_empty_list_for_unrated_contest(self):
        contest = models.Contest(id=21)  # unrated contest

        data = cf_api.get_rating_changes(contest)
        self.assertEqual(0, len(data))
