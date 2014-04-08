from django.db import models
from django.utils.timezone import now


class Project(models.Model):
    class Meta:
        pass

    name = models.CharField(max_length=50, unique=True)
    path = models.CharField(max_length=200, blank=True,
            help_text="Default is settings.WORKPLACE_PATH + project name")
    test_script = models.TextField()
    last_file_modified = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True, db_index=True)

    def get_last_history(self):
        if not hasattr(self, "_last_history"):
            try:
                self._last_history = self.history.latest()
            except ProjectHistory.DoesNotExist:
                return None
        return self._last_history

    def last_build(self):
        build = self.get_last_history()
        return build.started if build else ""

    def last_version(self):
        build = self.get_last_history()
        return build.version if build else ""

    def last_coverage(self):
        build = self.get_last_history()
        return build.coverage if build else ""

    def last_status(self):
        build = self.get_last_history()
        return build.status if build else ""

    def __unicode__(self):
        return self.name

    
class ProjectHistory(models.Model):
    class Meta:
        ordering = ("finished",)
        get_latest_by = "started"

    project = models.ForeignKey("Project", related_name="history")
    started = models.DateTimeField(default=now)
    finished = models.DateTimeField(null=True, blank=True)
    version = models.CharField(max_length=10, blank=True)
    coverage = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, blank=True)
    output = models.TextField(blank=True)

