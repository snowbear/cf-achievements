# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0004_add_Peresvet_and_Temir_Murza'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='rating',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='rewarding',
            name='contest',
            field=models.ForeignKey(null=True, to='achievements.Contest'),
            preserve_default=True,
        ),
    ]
