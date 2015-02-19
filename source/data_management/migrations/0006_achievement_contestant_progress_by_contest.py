# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0005_auto_20150210_1318'),
    ]

    operations = [
        migrations.RunSQL("""
CREATE TABLE data_management_achievement_contestant_progress_by_contest
(
   achievement_id integer NOT NULL, 
   contestant_id integer NOT NULL, 
   contest_id integer NOT NULL, 
   progress integer NOT NULL, 
   PRIMARY KEY (achievement_id, contestant_id, contest_id), 
   CONSTRAINT fk_achievement FOREIGN KEY (achievement_id) REFERENCES achievements_achievement (id) ON UPDATE NO ACTION ON DELETE NO ACTION, 
   CONSTRAINT fk_contestant FOREIGN KEY (contestant_id) REFERENCES achievements_contestant (id) ON UPDATE NO ACTION ON DELETE NO ACTION,
   CONSTRAINT fk_contest FOREIGN KEY (contest_id) REFERENCES achievements_contest (id) ON UPDATE NO ACTION ON DELETE NO ACTION
);
        """,
        "DROP TABLE data_management_achievement_contestant_progress_by_contest"),
    ]
