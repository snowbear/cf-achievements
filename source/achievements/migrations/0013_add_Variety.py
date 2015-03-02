# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from achievements.AddAchievementOperation import *
from achievements.achievement_data import *

class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0012_bitcount_function'),
    ]

    operations = [
        AddAchievementOperation(achievements.VARIETY_IS_THE_SPICE_OF_LIFE),
    ]
