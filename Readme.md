This is a very simple test builder for our Python projects.

1. Run "python manage.py syncdb"
2. Run "python manage.py runserver 0.0.0.0:7777"
3. Put in your crontab "python manage.py build_projects"
4. Access "http://localhost:7777/admin/apps/project", enter your user and password

### Missing

- To update the last version
