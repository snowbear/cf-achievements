from django import test

from achievements import models
from data_crawler.cf_api import get_submissions
from data_crawler.cf_api_enums import language_mapping


class Tests(test.TestCase):
    def test_can_map_languages(self):
        contest = models.Contest(id=537)  # contains zipped C++ and Java versions

        js_submissions = get_submissions(contest)
        for js_submission in js_submissions:
            language_mapping(js_submission['programmingLanguage'])
