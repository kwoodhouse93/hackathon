# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-03 15:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20170203_1508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='likes',
        ),
    ]
