# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('doctor', models.CharField(default='None', max_length=200)),
                ('length', models.IntegerField(blank=True, default=30, null=True)),
                ('date_time', models.DateTimeField(default=datetime.datetime.now)),
                ('reason_for_appointment', models.CharField(default='None', max_length=200)),
                ('additional_information', models.CharField(default='None', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('from_user', models.CharField(default='None', max_length=200)),
                ('to_user', models.CharField(default='None', max_length=200)),
                ('date_time', models.DateTimeField(default=datetime.datetime.now)),
                ('message', models.CharField(default='None', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(150)], default=0)),
                ('date_of_birth', models.DateField(default=datetime.datetime.now)),
                ('spouse_first_name', models.CharField(default='None', max_length=200)),
                ('next_of_kin', models.CharField(default='None', max_length=200)),
                ('emergency_contact', models.CharField(default='None', max_length=200)),
                ('ssn', models.SmallIntegerField(default=135234)),
                ('phone_number', models.CharField(validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message='Format +999999999.')], default='+999999999', max_length=15)),
                ('sex', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], default='', max_length=200)),
                ('weight', models.IntegerField(blank=True, default=0, null=True)),
                ('height', models.IntegerField(blank=True, default=0, null=True)),
                ('insurance', models.CharField(default='None', max_length=200)),
                ('prescription', models.CharField(default='None', max_length=200)),
                ('hospital', models.ForeignKey(to='healthnet.Hospital')),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='location',
            field=models.ForeignKey(to='healthnet.Hospital'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
