from django.core.management.base import BaseCommand, CommandError

from YAAS_App.models import Bid
from YAAS_App.views import *
from datetime import datetime
class Command(BaseCommand):
    help = 'Resolves all auctions'

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

                bids = Bid.objects.filter(auction_id=auction).distinct()
                bidders = [b.bidder for b in bids]
                emails_addresses = list(set([b.email for b in bidders]))
                emails_addresses.append((auction.seller).email)
                sendEmail(mail_subject, msg, emails_addresses)
            self.stdout.write(self.style.SUCCESS('Successfully resolved auctions'))

        print("*************************************************************************")
        print("Automatic auction resolving process ends.")