# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from achievements.achievement_data import PERESVET

def add_achievement(apps, schema_editor):
    Achievement = apps.get_model("achievements", "achievement")
    Achievement.objects.create(id = PERESVET.id,
                               name = PERESVET.name,
                               description = PERESVET.description)

def remove_achievement(apps, schema_editor):
    Achievement = apps.get_model("achievements", "achievement")
    Achievement.objects.get(pk = PERESVET.id).delete()
    

class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0003_rewarding_date'),
    ]

    operations = [
        migrations.RunPython(add_achievement, reverse_code = remove_achievement),
    ]
