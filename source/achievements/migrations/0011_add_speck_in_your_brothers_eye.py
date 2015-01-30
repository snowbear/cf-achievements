# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from achievements.AddAchievementOperation import *
from achievements.achievement_data import *

class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0010_add_language_achievements'),
    ]

    operations = [
        AddAchievementOperation(SPECK_IN_YOUR_BROTHERS_EYE),
    ]
