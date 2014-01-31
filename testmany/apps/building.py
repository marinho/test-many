import os
import subprocess
import stat
import re
import fnmatch
import time
import datetime
from multiprocessing import Process
from django.utils.timezone import now
from django.conf import settings


def get_project_path(project):
    if project.path.startswith("/"):
        return project.path
    else:
        return os.path.join(settings.WORKPLACE_PATH, project.path or project.name)


def build_projects(projects, force=False):
    for project in projects:
        build_project(project, force)


def build_project(project, force=False):
    # Check if project files were modified
    if not force and not project_was_modified(project):
        print("Project %s was not modified" % project.name)
        return

    print("Started %s" % project.name)

    # New build
    build = project.history.create(
            status="building",
            )

    def _inner(build):
        curdir = os.path.abspath(os.curdir)
        os.chdir(get_project_path(project))

        # Temporary script
        temp_file = ".temp_test_script.sh"
        fp = file(temp_file, "w")
        fp.write(project.test_script.replace("\r", ""))
        fp.close()
        os.chmod(temp_file, stat.S_IEXEC | stat.S_IWRITE | stat.S_IREAD)

        # Running command
        output = subprocess.check_output("./.temp_test_script.sh")
        f = re.findall("TOTAL[ ]+\d+?[ ]+\d+?[ ]+(\d+?)%", output)
        coverage = int(f[0]) if f else None

        # Result
        build.coverage = coverage
        build.output = output
        build.finished = now()
        build.status = "passed" if coverage else "failed"
        build.save()

        project.last_file_modified = now()
        project.save()

        print("Finished %s: %s" % (project.name, build.status))

        # Returns to previous state
        os.unlink(temp_file)
        os.chdir(curdir)

    proc = Process(target=_inner, args=(build,))
    proc.start()


def project_was_modified(project):
    if not project.last_file_modified:
        return True

    curdir = os.path.abspath(os.curdir)
    os.chdir(get_project_path(project))
    project_mtime = time.mktime(project.last_file_modified.timetuple())
    last_mtime = 0

    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.py'):
            file_path = os.path.join(root, filename)
            statbuf = os.stat(file_path)
            last_mtime = max([last_mtime, statbuf.st_mtime])

    os.chdir(curdir)
    return last_mtime > project_mtime
