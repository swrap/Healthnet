# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0014_auto_20151205_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientfile',
            name='file_name',
            field=models.CharField(default='None', max_length=200),
        ),
    ]
