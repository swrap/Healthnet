# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0006_prescription_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_in_hospital',
            field=models.BooleanField(default=False),
        ),
    ]
