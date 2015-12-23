# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0011_auto_20151205_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
