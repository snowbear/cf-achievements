# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from achievements.AddAchievementOperation import *
from achievements.achievement_data import *

class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0009_contest_order'),
    ]

    operations = [
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_C),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_CPP),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_CS),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_D),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_GO),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_HASKELL),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_JAVA),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_OCAML),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_PASCAL),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_PERL),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_PHP),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_PYTHON),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_RUBY),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_SCALA),
        AddAchievementOperation(LANGUAGE_ACHIEVEMENT_JAVASCRIPT),
    ]
