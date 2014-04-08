import os
from django.core.management import BaseCommand
from apps.models import Project
from apps.building import build_projects
from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--project', action='store', dest='project', default=None),
    )

    def handle(self, project=None, **kwargs):
        if project:
            projects = Project.objects.filter(name=project)
        else:
            projects = Project.objects.filter(active=True)

        build_projects(projects, bool(project))
