from django.contrib import admin
from models import Project, ProjectHistory
from building import build_projects


class ProjectHistoryInline(admin.TabularInline):
    model = ProjectHistory
    readonly_fields = ("started", "finished", "version", "coverage", "status")
    exclude = ("output",)
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectHistoryInline]
    list_display = ["name", "last_build", "last_version", "last_coverage", "last_status", "active"]
    list_filter = ("active",)
    actions = ["run_builds"]
    readonly_fields = ("last_file_modified",)

    def run_builds(self, request, queryset):
        build_projects(queryset, force=True)
    run_builds.short_description = "Build selected proects"


admin.site.register(Project, ProjectAdmin)

