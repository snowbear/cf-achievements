from django.db import models
from django.shortcuts import get_object_or_404

from achievements.models import Achievement, Contest

class AchievementParseProgress_ByContest(models.Model):
    achievement = models.ForeignKey(Achievement, unique = True)
    lastParsedContest = models.ForeignKey(Contest, null = True)

    def __str__(self):
        return self.achievement.name

    def get_for_achievement(achievementId):
        achievement_obj = get_object_or_404(Achievement, pk = achievementId)
        return AchievementParseProgress_ByContest.objects.get_or_create(achievement = achievement_obj)[0]
