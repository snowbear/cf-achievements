from django.db import models
from django.shortcuts import get_object_or_404

from achievements.models import *

class AchievementParseProgress_ByContest(models.Model):
    achievement = models.ForeignKey(Achievement, unique = True)
    lastParsedContest = models.ForeignKey(Contest, null = True, on_delete = models.PROTECT)

    def __str__(self):
        return self.achievement.name

    def get_for_achievement(achievementId):
        achievement_obj = get_object_or_404(Achievement, pk = achievementId)
        return AchievementParseProgress_ByContest.objects.get_or_create(achievement = achievement_obj)[0]

class ContestParticipation(models.Model):
    contest = models.ForeignKey(Contest)
    contestant = models.ForeignKey(Contestant)
    participant_type = models.IntegerField()
    taken_place = models.IntegerField(null = True)
    successful_hacks = models.IntegerField()
    unsuccessful_hacks = models.IntegerField()
    rating_before = models.IntegerField(null = True)
    rating_after = models.IntegerField(null = True)
    room = models.IntegerField(null = True)
    class Meta:
        unique_together = ('contest' , 'contestant')
        
class Problem(models.Model):
    contest = models.ForeignKey(Contest)
    index = models.CharField(max_length = 5)
    order = models.IntegerField()
    name = models.CharField(max_length = 200)
    points = models.FloatField(null = True)
    
    class Meta:
        unique_together = ('contest' , 'index')
        
class Submission(models.Model):
    id = models.IntegerField(primary_key = True)
    contest = models.ForeignKey(Contest)
    creation_time_seconds = models.IntegerField()
    relative_time_seconds = models.IntegerField()
    problem = models.ForeignKey(Problem)
    author = models.ForeignKey(Contestant)
    language = models.IntegerField()
    verdict = models.IntegerField()
    testset = models.IntegerField()
    passed_test_count = models.IntegerField()
    time_consumed_milliseconds = models.IntegerField()
    memory_consumed_bytes = models.IntegerField()
        
class Hack(models.Model):
    hacker = models.ForeignKey(Contestant, related_name = '+')
    defender = models.ForeignKey(Contestant, related_name = '+')
    problem = models.ForeignKey(Problem)
    challenged_submission = models.ForeignKey(Submission, null = True)
    creation_time_seconds = models.IntegerField()
    verdict = models.IntegerField()
    test_size = models.IntegerField()
    is_manual = models.BooleanField()
    
class Task(models.Model):
    name = models.CharField(max_length = 20)
    additional_id = models.IntegerField(null = True)
    added_on = models.DateTimeField()
    finished_on = models.DateTimeField(null = True)
    
    UPDATE_RATINGS = "update ratings"
    LOAD_DATA = "load data"
    UPDATE_ACHIEVEMENTS = "update achievements"