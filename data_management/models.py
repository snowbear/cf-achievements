from django.db import models
from django.shortcuts import get_object_or_404

from achievements.models import Achievement, Contest

class AchievementParseProgress_ByContest(models.Model):
    achievement = models.ForeignKey(Achievement, unique = True)
    lastParsedContest = models.ForeignKey(Contest, null = True, on_delete = models.PROTECT)

    def __str__(self):
        return self.achievement.name

    def get_for_achievement(achievementId):
        achievement_obj = get_object_or_404(Achievement, pk = achievementId)
        return AchievementParseProgress_ByContest.objects.get_or_create(achievement = achievement_obj)[0]

class temp_user_rating(models.Model):
    tmp_handle = models.CharField(max_length=200, primary_key = True)
    tmp_rating = models.IntegerField()