from __future__ import absolute_import
import os
import re

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from django.apps import apps

def read_env():
    """Pulled from Honcho code with minor updates, reads local default
    environment variables from a .env file located in the project root
    directory.
    """
    try:
        with open('.env') as f:
            content = f.read()
    except IOError:
        content = ''
    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)


read_env()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authentication.settings')
app = Celery('authentication', include=["accounts.task"])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object(settings, namespace="CELERY")

# app.conf.beat_schedule = {
#     'twitter-every-45-minutes': {
#         'task': 'media_fetchers.tasks.twitter_fetcher',
#         'schedule': crontab(minute='*/45'),
#         'args': ()
#     },
#
#     'twitter-curated-every-30-minutes': {
#         'task': 'media_fetchers.tasks.curated_twitter_fetcher',
#         'schedule': crontab(minute='*/30'),
#         'args': ()
#     },
#
#     'twitter-realtime-every-30-minutes': {
#         'task': 'media_fetchers.tasks.twitter_realtime',
#         'schedule': crontab(minute='*/1'),
#         'args': ()
#     },
#
#     'elephant-every-45-minutes': {
#         'task': 'media_fetchers.tasks.elephant_scheduler',
#         'schedule': crontab(minute='*/45'),
#         'args': ()
#     },
#
#     'youtube-channel-every-45-minutes': {
#         'task': 'media_fetchers.tasks.youtube_channel_fetcher',
#         'schedule': crontab(minute='*/45'),
#         'args': ()
#     },
#
#     'youtube_curated_channel_every_30_minutes': {
#         'task': 'media_fetchers.tasks.youtube_curated_channel',
#         'schedule': crontab(minute='*/30'),
#         'args': ()
#     },
#
#     # 'categorizing': {
#     #     'task': 'media_fetchers.tasks.content_categorization',
#     #     'schedule': crontab(minute='*/30'),
#     #     'args': ()
#     # },
#
# }

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
