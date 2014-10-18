from django.db import models

class Contestant(models.Model):
    handle = models.CharField(max_length=200, unique = True)
    rating = models.IntegerField(null = True)

    def __str__(self):
        return self.handle

class Contest(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=200)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Achievement(models.Model):
    id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class Rewarding(models.Model):
    participant = models.ForeignKey(Contestant)
    achievement = models.ForeignKey(Achievement)
    comment = models.CharField(max_length=1000)
    date = models.DateTimeField()
    contest = models.ForeignKey(Contest, null = True)
    level = models.IntegerField(null = True)

    def __str__(self):
        return self.participant.handle + " - " + self.achievement.name