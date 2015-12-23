# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='location',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='hospital',
            field=models.ForeignKey(to='healthnet.Hospital', blank=True, default=1),
        ),
    ]
