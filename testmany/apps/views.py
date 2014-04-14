import json
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.utils import timesince
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

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


@csrf_exempt
def push_info(request):
    package = request.POST["package"]
    version = request.POST["version"]
    coverage = request.POST["coverage"]
    status = request.POST["status"]

    project = get_object_or_404(Project, name=package)

    project.history.create(
        finished = now(),
        version = version,
        coverage = int(coverage),
        status = status,
        )

    return HttpResponse("OK", content_type="text/plain")
