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

    def test_get_rating_changes_returns_empty_list_for_private_contest(self):
        contest = models.Contest(id=726)  # private contest

        data = cf_api.get_rating_changes(contest)
        self.assertEqual(0, len(data))

    def test_is_private_contest_returns_true_for_private_contest(self):
        contest = models.Contest(id=726)
        self.assertTrue(cf_api.is_private_contest(contest))

    def test_is_private_contest_returns_false_for_regular_contest(self):
        contest = models.Contest(id=1)
        self.assertFalse(cf_api.is_private_contest(contest))
