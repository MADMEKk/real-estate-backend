from __future__ import absolute_import

import os

from celery import Celery
from project_name import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','project_name.settings')

app = Celery('project_name')

app.config_from_object('project_name.settings',
                       namespace="CELERY"),
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
