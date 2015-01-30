# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0002_auto_20141017_0302'),
    ]

    operations = [
        migrations.DeleteModel(
            name='temp_user_rating',
        ),
    ]
