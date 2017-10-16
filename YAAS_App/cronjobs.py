from YAAS_App.models import Auction

__author__ = 'selab'

from django_cron import CronJobBase, Schedule
from django.shortcuts import get_object_or_404
#from auction.models import Auction
from datetime import datetime

class CronJob(CronJobBase):
    RUN_EVERY_MINS = 1
    #'11:30', '14:00', '23:15'

    #RUN_AT_TIMES = [runtimes]
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'YAAS_App.cron_job'    # a unique code

    def do(self):
        #auction = get_object_or_404(a)
        auctions=Auction.objects.all()
        print(datetime.now().strftime('%Y-%m-%d %H:%M'))
        for auction in auctions:
            print(auction.endtime.strftime('%Y-%m-%d %H:%M') )
            #print(datetime.now())
            if auction.endtime.strftime('%Y-%m-%d %H:%M') == datetime.now().strftime('%Y-%m-%d %H:%M'):
                auction.auction_status='D'
                print('Auction ended')



