from __future__ import absolute_import

import os

from celery import Celery

from organicFood.settings import base

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "organicFood.settings.development")

app = Celery("organic_food")

app.config_from_object("organicFood.settings.development", namespace="CELERY"),

app.autodiscover_tasks(lambda: base.INSTALLED_APPS)
