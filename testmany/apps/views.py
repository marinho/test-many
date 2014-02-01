import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import timesince

from apps.models import Project


def index(request):
    return render_to_response("apps/index.html")


def projects_json(request):
    projects = Project.objects.filter(active=True)
    data = {
        "result": "ok",
        "projects": map(format_project, projects),
    }
    return HttpResponse(json.dumps(data), content_type="text/json")


def format_project(project):
    return {
        "name": project.name,
        "last_build": timesince.timesince(project.last_build()) if project.last_build() else "",
        "version": project.last_version(),
        "coverage": project.last_coverage(),
        "status": project.last_status(),
    }
