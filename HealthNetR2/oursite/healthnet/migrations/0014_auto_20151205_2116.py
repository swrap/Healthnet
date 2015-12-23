# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthnet', '0013_patientfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientfile',
            name='patient_file',
            field=models.FileField(upload_to='patient/fileuploads/'),
        ),
    ]
