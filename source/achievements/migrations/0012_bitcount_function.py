# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0011_add_speck_in_your_brothers_eye'),
    ]

    operations = [
        migrations.RunSQL("""
CREATE FUNCTION bitcount(i integer) RETURNS integer AS $$
DECLARE n integer;
DECLARE amount integer;
  BEGIN
    amount := 0;
    FOR n IN 1..32 LOOP
      amount := amount + ((i >> (n-1)) & 1);
    END LOOP;
    RETURN amount;
  END
$$ LANGUAGE plpgsql;
        """,
        "DROP FUNCTION bitcount(integer)"),
    ]
