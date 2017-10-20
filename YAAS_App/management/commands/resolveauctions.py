from django.core.management.base import BaseCommand, CommandError
from YAAS_App.views import *
from datetime import datetime
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)
        pass
    def handle(self, *args, **options):
        print("Automatic auction resolving process starts.")
        print("*******************************************************")
        auctions = Auction.objects.all()
        #print(datetime.now().strftime('%Y-%m-%d %H:%M'))
        for auction in auctions:
            #print(auction.endtime.strftime('%Y-%m-%d %H:%M'))
            # print(datetime.now())
            if auction.auction_status == 'A' and check_endingtime(auction.endtime) or auction.auction_status == 'C':
                auction.auction_status = 'D'
                auction.save()

                mail_subject = "Auction " + str(auction.title) + " is resolved by the system."
                msg = "Auction " + str(auction.title) + " is resolved."

                pids = Pid.objects.filter(auction_id=auction).distinct()
                pidders = [p.pidder for p in pids]
                emails_addresses = list(set([p.email for p in pidders]))
                emails_addresses.append((auction.seller).email)
                sendEmail(mail_subject, msg, emails_addresses)
            self.stdout.write(self.style.SUCCESS('Successfully resolved auctions'))

        print("*************************************************************************")
        print("Automatic auction resolving process ends.")