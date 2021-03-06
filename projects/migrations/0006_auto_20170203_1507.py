# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-03 15:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20170202_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='likes',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='participating_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='participant', to=settings.AUTH_USER_MODEL),
        ),
    ]
