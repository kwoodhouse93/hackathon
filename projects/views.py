from datetime import date

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from helpers import *
from .models import Project
from .models import Hackathon
from django.contrib.auth.models import User

from .forms import ProjectForm, ReviewForm

def index(request, hackathon=None):
    # import pdb
    if hackathon is None:
        hackathon = decide_which_hackathon_to_display()
    if hackathon:
        projects = Project.objects.filter(hackathon__number = hackathon).annotate(p_count=Count('participating_users')).order_by('-p_count')
        if request.user.is_authenticated() and user_participating_in_projects(projects, request.user):
            user_participating_already = True
            current_users_project_qs = request.user.participant.filter(hackathon_id=hackathon)
            if current_users_project_qs.count() > 0:
                current_users_project = current_users_project_qs[0]
        else:
            user_participating_already = False
            current_users_project = None

        today = date.today()
        hackathon_open = Hackathon.objects.get(number=hackathon).end_date > today

        hackathon_object = Hackathon.objects.get(number=hackathon)

        start_date = hackathon_object.start_date.strftime('%b. %d')
        end_date = hackathon_object.end_date.strftime('%b. %d')
        year = hackathon_object.end_date.strftime('%Y')
    else:
        projects = Project.objects.all().annotate(p_count=Count(participating_users)).order_by('-p_count')
        user_participating_already = False
        current_users_project = None
        hackathon_open = False
        start_date = None
        end_date = None
        year = None

    hackathons = decide_which_hackathons_to_display(4)
    authenticated = request.user.is_authenticated()
    context = {
        'projects': projects,
        'hackathon': hackathon,
        'hackathons': hackathons,
        'user_participating_already': user_participating_already,
        'current_users_project': current_users_project,
        'authenticated': authenticated,
        'hackathon_open': hackathon_open,
        'start_date': start_date,
        'end_date': end_date,
        'year': year,
    }
    return render(request, 'projects/index.html', context)

def project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    today = date.today()
    hackathon_open = project.hackathon.end_date > today

    if request.method == 'POST':
        if "leave" in request.POST:
            project.participating_users.remove(request.user)
            current_user_participating = False
        if "join" in request.POST:
            project.participating_users.add(request.user)
            current_user_participating = True

        redirect_url = "/projects/" + str(project_id)
        return HttpResponseRedirect(redirect_url, {'project':project, 'current_user_participating':current_user_participating})

    authenticated = request.user.is_authenticated()

    if authenticated:
        current_user_participating = request.user.participant.filter(id=project.id).exists()
        user_participating_already = user_participating_in_hackathon(project.hackathon.number, request.user)
    else:
        current_user_participating = False
        user_participating_already = False

    context = {
        'project': project,
        'current_user_participating': current_user_participating,
        'user_participating_already': user_participating_already,
        'authenticated': authenticated,
        'hackathon_open': hackathon_open,
    }

    return render(request, 'projects/project.html', context)

@login_required
def add_project(request):
    userFullName = request.user.first_name + ' ' + request.user.last_name
    form = ProjectForm(request.POST or None, initial={'hackathon': decide_which_hackathon_to_display(), 'author': userFullName})
    if request.method == 'POST':
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            # Sign me up automatically IFF:
            #    I'm the leader of the project
            #    I haven't already joined another project this hackathon
            if (project.author.strip() == request.user.get_full_name() and
                    not user_participating_in_hackathon(project.hackathon.number, request.user)
                ):
                project.participating_users.add(request.user)
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
            # Sign me up automatically IFF:
            #    I'm the leader of the project
            #    I haven't already joined another project this hackathon
            if (project.author.strip() == request.user.get_full_name() and
                    not user_participating_in_hackathon(project.hackathon.number, request.user)
                ):
                project.participating_users.add(request.user)
        return HttpResponseRedirect("/projects/")

    context = {
        "form": form,
        "project": project
    }

    return render(request, "projects/edit.html", context)


def review(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    authenticated = request.user.is_authenticated()

    if authenticated:
        current_user_participating = request.user.participant.filter(id=project.id).exists()
    else:
        current_user_participating = None

    context = {
        'project': project,
        'authenticated': authenticated,
        'current_user_participating': current_user_participating,
    }

    return render(request, 'projects/review.html', context)

@login_required
def edit_review(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    #FORM
    form = ReviewForm(request.POST or None, instance=project)
    if form.is_valid():
        project = form.save(commit=False)
        project.save()

        url = reverse('projects:review', kwargs={'project_id': project_id})
        return HttpResponseRedirect(url)

    context = {
        'form':form,
        'project': project,
    }

    return render(request, 'projects/edit_review.html', context)

def showcase(request, hackathon=None):
    if hackathon is None:
        hackathon = decide_which_hackathon_to_display()
    if hackathon:
        projects = Project.objects.filter(hackathon__number = hackathon)
        if request.user.is_authenticated() and user_participating_in_projects(projects, request.user):
            current_users_project_qs = request.user.participant.filter(hackathon_id=hackathon)
            if current_users_project_qs.count() > 0:
                current_users_project = current_users_project_qs[0]
        else:
            current_users_project = None

        hackathon_object = Hackathon.objects.get(number=hackathon)
        start_date = hackathon_object.start_date.strftime('%b. %d')
        end_date = hackathon_object.end_date.strftime('%b. %d')
        year = hackathon_object.end_date.strftime('%Y')
    else:
        projects = Project.objects.all()
        current_users_project = None
        start_date = None
        end_date = None
        year = None

    # All past hackathons
    today = date.today()
    hackathons = Hackathon.objects.filter(end_date__lte=today)

    context = {
        'hackathon': hackathon,
        'hackathons': hackathons,
        'projects': projects,
        'current_users_project': current_users_project,
        'start_date': start_date,
        'end_date': end_date,
        'year': year,
    }

    return render(request, 'projects/showcase.html', context)