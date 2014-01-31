from django.core.management import BaseCommand
from apps.models import Project
from apps.building import build_projects


class Command(BaseCommand):
    def handle(self, **kwargs):
        projects = Project.objects.filter(active=True)
        build_projects(projects)
