# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-02 11:04
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='showcase_aims',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='showcase_future_work',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='showcase_lessons',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AddField(
            model_name='project',
            name='showcase_summary',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
    ]
