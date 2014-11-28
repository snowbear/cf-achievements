# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0008_add_Language_does_not_matter'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='order',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]
