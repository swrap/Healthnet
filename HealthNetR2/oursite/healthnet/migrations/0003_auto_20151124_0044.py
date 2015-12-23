# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('healthnet', '0002_auto_20151118_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('previous_employment', models.CharField(max_length=200, default='None')),
                ('degree', models.CharField(max_length=200, default='None')),
                ('hospital', models.ManyToManyField(to='healthnet.Hospital')),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('previous_employment', models.CharField(max_length=200, default='None')),
                ('degree', models.CharField(max_length=200, default='None')),
                ('hospital', models.ForeignKey(default=1, blank=True, to='healthnet.Hospital')),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='doctor',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='doctor',
            field=models.ForeignKey(default=1, blank=True, to='healthnet.DoctorProfile'),
        ),
    ]
