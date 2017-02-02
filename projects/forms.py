from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext_lazy as _
from projects.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model  = Project
        fields = ('name', 'hackathon', 'rich_description', 'author', 'min_participants', 'max_participants', 'skills', 'tags')
        widgets = {
            'skills': TextInput(),
            'tags': TextInput(),
        }
        initial = {
            'min_participants': 1,
            'max_participants': 1,
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Project
        fields = ('showcase_aims', 'showcase_summary', 'showcase_lessons', 'showcase_future_work')