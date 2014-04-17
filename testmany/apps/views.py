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


COVERAGE_BADGE_TPL = """
<svg xmlns="http://www.w3.org/2000/svg" width="98" height="18">
 <linearGradient id="a" x2="0" y2="100%%">
  <stop offset="0" stop-color="#fff" stop-opacity=".7"/>
  <stop offset=".1" stop-color="#aaa" stop-opacity=".1"/>
  <stop offset=".9" stop-opacity=".3"/>
  <stop offset="1" stop-opacity=".5"/>
 </linearGradient>
 <rect rx="4" width="98" height="18" fill="#555"/>
 <rect rx="4" x="59" width="39" height="18" fill="%(color)s"/>
 <rect rx="4" width="98" height="18" fill="url(#a)"/>
 <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
  <text x="29.5" y="13" fill="#010101" fill-opacity=".3">coverage</text>
  <text x="29.5" y="12">coverage</text>
  <text x="78" y="13" fill="#010101" fill-opacity=".3">%(coverage)s%%</text>
  <text x="78" y="12">%(coverage)s%%</text>
 </g>
</svg>
"""

def coverage_badge(request, package):
    project = get_object_or_404(Project, name=package)
    coverage_percent = project.last_coverage()
    if coverage_percent >= 100:
        color = "#00f"
    elif coverage_percent >= 80:
        color = "#0c0"
    elif coverage_percent >= 60:
        color = "#cc0"
    else:
        color = "#f00"

    svg = COVERAGE_BADGE_TPL % {
        "color": color,
        "coverage": coverage_percent,
        }
    return HttpResponse(svg.strip(), content_type="image/svg+xml")
