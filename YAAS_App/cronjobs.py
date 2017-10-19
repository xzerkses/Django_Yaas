from YAAS_App.models import Auction
from YAAS_App.views import *
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
            if auction.auction_status=='A' and check_endingtime(auction.endtime) or auction.auction_status=='C':
                auction.auction_status='D'
                auction.latest_pid
                pids=Pid.objects.filter(auction_id=auction)
                pids
                mail_subject = "Auction " + str(auction.title) + " is resolved by the system."
                msg = "Auction " + str(auction.title) + " is resolved. Winner is"

                pids = Pid.objects.filter(auction_id=auction).distinct()
                pidders = [p.pidder for p in pids]
                emails_addresses = list(set([p.email for p in pidders]))
                emails_addresses.append((auction.seller).email)
                sendEmail(mail_subject, msg, emails_addresses)


