from __future__ import unicode_literals

import re

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.auth.models import User
from hackathons.models import Hackathon

@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(max_length=240)
    description = models.TextField(null=True, blank=True) # Deprecated
    rich_description = RichTextUploadingField(default="")
    author = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # led_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.TextField(blank=True) # Deprecated
    participating_users = models.ManyToManyField(User, related_name='participant')
    min_participants = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    max_participants = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    hackathon = models.ForeignKey(Hackathon, on_delete=models.SET_NULL, null=True, blank=True)
    skills = models.TextField(blank=True)
    tags = models.TextField(blank=True)
    # Fields for the showcase:
    showcase_aims = RichTextUploadingField(default="", null=True, blank=True)
    showcase_summary = RichTextUploadingField(default="", null=True, blank=True)
    showcase_lessons = RichTextUploadingField(default="", null=True, blank=True)
    showcase_future_work = RichTextUploadingField(default="", null=True, blank=True)



    def __str__(self):
        return self.name

    def spaces_left(self):
        return self.participating_users.count() < self.max_participants

    def participants_needed(self):
        return self.participating_users.count() > self.min_participants

    def tag_list(self):
        return filter(bool, re.split('[,;]', self.tags))

    def skills_list(self):
        return filter(bool, re.split('[,;]', self.skills))


