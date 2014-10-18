# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from achievements.AddAchievementOperation import *
from achievements.achievement_data import POLYGLOT

class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0005_auto_20141016_2315'),
    ]

    operations = [
        AddAchievementOperation(POLYGLOT),
    ]
