# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='temp_user_rating',
            fields=[
                ('tmp_handle', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('tmp_rating', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='achievementparseprogress_bycontest',
            name='lastParsedContest',
            field=models.ForeignKey(to='achievements.Contest', on_delete=django.db.models.deletion.PROTECT, null=True),
        ),
    ]
