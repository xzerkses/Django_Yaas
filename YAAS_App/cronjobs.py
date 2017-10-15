__author__ = 'selab'

from django_cron import CronJobBase, Schedule
from django.shortcuts import get_object_or_404
from blogApp.models import BlogPost
from datetime import datetime

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'blogApp.my_cron_job'    # a unique code

    def do(self):
        blog = get_object_or_404(BlogPost, id = 1,)
        blog.body = str(datetime.now())
        blog.save()
        print("I am running!")
