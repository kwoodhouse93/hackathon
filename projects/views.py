from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.db.models import Max
from django.contrib.auth.decorators import login_required

from helpers import *
from .models import Project
from .models import Hackathon
from django.contrib.auth.models import User

from .forms import ProjectForm

def index(request, hackathon=None):
    # import pdb
    if hackathon is None:
        hackathon = decide_which_hackathon_to_display()
    if hackathon:
        projects = Project.objects.filter(hackathon__number = hackathon)
        if request.user.is_authenticated() and user_participating_in_projects(projects, request.user):
            user_participating_already = True
            current_users_project_qs = request.user.participant.filter(hackathon_id=hackathon)
            if current_users_project_qs.count > 0:
                current_users_project = current_users_project_qs[0]
        else:
            user_participating_already = False
            current_users_project = None
    else:
        projects = Project.objects.all()
    hackathons = decide_which_hackathons_to_display(4)
    context = {
        'projects': projects,
        'hackathon': hackathon,
        'hackathons': hackathons,
        'user_participating_already': False,
        'current_users_project': None,
    }
    # pdb.set_trace()
    return render(request, 'projects/index.html', context)

def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        if "leave" in request.POST:
            project.participating_users.remove(request.user)
            current_user_participating = False
        if "join" in request.POST:
            project.participating_users.add(request.user)
            current_user_participating = True
        redirect_url = "/projects/" + str(project_id)
        return HttpResponseRedirect(redirect_url, {'project':project, 'current_user_participating':current_user_participating})

    if request.user.is_authenticated():
        current_user_participating = request.user.participant.filter(id=project.id).exists()
        user_participating_already = user_participating_in_hackathon(project.hackathon.number, request.user)
    else:
        current_user_participating = False
        user_participating_already = False

    context = {
        'project':project,
        'current_user_participating':current_user_participating,
        'user_participating_already':user_participating_already,
    }

    return render(request, 'projects/project.html', context)

@login_required
def add_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return HttpResponseRedirect("/projects/")
    context = {
        "form": form
    }

    return render(request, "projects/add.html", context)

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        if "delete" in request.POST:
            project.delete()
        else:
            project = form.save(commit=False)
            project.save()
        return HttpResponseRedirect("/projects/")

    context = {
        "form": form,
        "project": project
    }

    return render(request, "projects/edit.html", context)
