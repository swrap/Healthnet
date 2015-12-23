# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0009_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='to_hospital',
            field=models.ForeignKey(default=1, blank=True, to='healthnet.Hospital'),
        ),
    ]
