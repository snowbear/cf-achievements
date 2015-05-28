# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0007_task'),
    ]

    operations = [
        migrations.RunSQL("DROP TABLE data_management_achievement_contestant_progress"),
    ]
