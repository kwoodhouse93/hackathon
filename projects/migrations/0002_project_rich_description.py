# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-16 16:06
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='rich_description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
    ]
