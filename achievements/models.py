from django.db import models

class Contestant(models.Model):
    handle = models.CharField(max_length=200)

    def __str__(self):
        return self.handle

class Contest(models.Model):
    name = models.CharField(max_length=100)
    cfId = models.IntegerField('Codeforces Contest Id')
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

class Rewarding(models.Model):
    participant = models.ForeignKey(Contestant)
    achievement = models.ForeignKey(Achievement)
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.participant.handle + " - " + self.achievement.name

