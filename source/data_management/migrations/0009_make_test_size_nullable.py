# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0008_drop_achievement_contestant_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hack',
            name='test_size',
            field=models.IntegerField(null=True),
        ),
    ]
