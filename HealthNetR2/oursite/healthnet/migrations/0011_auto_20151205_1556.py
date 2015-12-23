# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0010_auto_20151205_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='prescribed_by_doctor',
            field=models.ForeignKey(null=True, to='healthnet.DoctorProfile'),
        ),
        migrations.AddField(
            model_name='test',
            name='prescribed_by_doctor',
            field=models.ForeignKey(null=True, to='healthnet.DoctorProfile'),
        ),
    ]
