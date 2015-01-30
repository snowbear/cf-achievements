# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0002_add_Did_not_scratch_me_achievement'),
    ]

    operations = [
        migrations.AddField(
            model_name='rewarding',
            name='date',
            field=models.DateTimeField(default=timezone.now()),
            preserve_default=False,
        ),
    ]
