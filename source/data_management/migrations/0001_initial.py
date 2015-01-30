# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AchievementParseProgress_ByContest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('achievement', models.ForeignKey(unique=True, to='achievements.Achievement')),
                ('lastParsedContest', models.ForeignKey(to='achievements.Contest', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
