# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0011_add_speck_in_your_brothers_eye'),
        ('data_management', '0004_achievement_contestant_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestParticipation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('participant_type', models.IntegerField()),
                ('taken_place', models.IntegerField(null=True)),
                ('successful_hacks', models.IntegerField()),
                ('unsuccessful_hacks', models.IntegerField()),
                ('rating_before', models.IntegerField(null=True)),
                ('rating_after', models.IntegerField(null=True)),
                ('room', models.IntegerField(null=True)),
                ('contest', models.ForeignKey(to='achievements.Contest')),
                ('contestant', models.ForeignKey(to='achievements.Contestant')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hack',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('creation_time_seconds', models.IntegerField()),
                ('verdict', models.IntegerField()),
                ('test_size', models.IntegerField()),
                ('is_manual', models.BooleanField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('index', models.CharField(max_length=5)),
                ('order', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('points', models.FloatField(null=True)),
                ('contest', models.ForeignKey(to='achievements.Contest')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('creation_time_seconds', models.IntegerField()),
                ('relative_time_seconds', models.IntegerField()),
                ('language', models.IntegerField()),
                ('verdict', models.IntegerField()),
                ('testset', models.IntegerField()),
                ('passed_test_count', models.IntegerField()),
                ('time_consumed_milliseconds', models.IntegerField()),
                ('memory_consumed_bytes', models.IntegerField()),
                ('author', models.ForeignKey(to='achievements.Contestant')),
                ('contest', models.ForeignKey(to='achievements.Contest')),
                ('problem', models.ForeignKey(to='data_management.Problem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='problem',
            unique_together=set([('contest', 'index')]),
        ),
        migrations.AddField(
            model_name='hack',
            name='challenged_submission',
            field=models.ForeignKey(null=True, to='data_management.Submission'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hack',
            name='defender',
            field=models.ForeignKey(to='achievements.Contestant', related_name='+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hack',
            name='hacker',
            field=models.ForeignKey(to='achievements.Contestant', related_name='+'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hack',
            name='problem',
            field=models.ForeignKey(to='data_management.Problem'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contestparticipation',
            unique_together=set([('contest', 'contestant')]),
        ),
    ]
