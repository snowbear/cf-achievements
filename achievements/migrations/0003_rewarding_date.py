# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0002_add_Did_not_scratch_me_achievement'),
    ]

    operations = [
        migrations.AddField(
            model_name='rewarding',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 4, 0, 1)),
            preserve_default=False,
        ),
    ]
