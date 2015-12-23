# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0003_auto_20151124_0044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctorprofile',
            old_name='degree',
            new_name='accreditation',
        ),
        migrations.RenameField(
            model_name='staffprofile',
            old_name='degree',
            new_name='accreditation',
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='education_information',
            field=models.CharField(max_length=200, default='None'),
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='licenses',
            field=models.CharField(max_length=200, default='None'),
        ),
        migrations.AddField(
            model_name='staffprofile',
            name='education_information',
            field=models.CharField(max_length=200, default='None'),
        ),
        migrations.AddField(
            model_name='staffprofile',
            name='licenses',
            field=models.CharField(max_length=200, default='None'),
        ),
    ]
