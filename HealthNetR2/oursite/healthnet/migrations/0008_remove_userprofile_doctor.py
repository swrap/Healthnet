# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0007_userprofile_is_in_hospital'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='doctor',
        ),
    ]
