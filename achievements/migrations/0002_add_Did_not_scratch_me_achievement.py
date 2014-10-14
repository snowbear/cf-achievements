# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from achievements.achievement_data import DID_NOT_SCRATCH_ME

def add_achievement(apps, schema_editor):
    Achievement = apps.get_model("achievements", "achievement")
    Achievement.objects.create(id = DID_NOT_SCRATCH_ME.id,
                               name = DID_NOT_SCRATCH_ME.name,
                               description = DID_NOT_SCRATCH_ME.description)

def remove_achievement(apps, schema_editor):
    Achievement = apps.get_model("achievements", "achievement")
    Achievement.objects.get(pk = 1).delete()
    

class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_achievement, reverse_code = remove_achievement),
    ]
