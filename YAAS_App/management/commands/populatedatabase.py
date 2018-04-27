import datetime
import random
import string

from django.core.management import BaseCommand

from YAAS_App.models import Pid, Auction,User


class Command(BaseCommand):


    def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)
        pass
    def handle(self, *args, **options):

        self.usernames = ['jimbo', 'monkey', 'cora', 'zorro', 'benny', 'maya', 'aztec', 'carol', 'omar', 'rolf']
        self.email_suffixes = ['shop.fi', 'fmail.fi', 'eshop.fi', 'market.fi', 'testmail.fi']
        self.items=['Bicycle', 'Hand Saw', 'Hand Plane', 'Hammer', 'Window','Statue','Nail']

        self.create_users(50)
        self.create_auctions(50)
        self.create_pids()

    def create_users(self, count):
        for i in range(count):
            new_user =self.generate_username()

            new_email = new_user + self.email_suffixes[len(self.email_suffixes)-1]

            passwrd = self.psswrd_generator(8)
            print("Adding a user named ", new_user )
            User.objects.create_user(username=new_user, email=new_email, password=passwrd)

    def generate_username(self):
        user=self.usernames[random.randint(0, len(self.usernames) - 1)]

        while User.objects.filter(username=user).exists():
            user=user+'_'+self.psswrd_generator(2)

        return user



    def psswrd_generator(self,count):
        psswrd=''
        for i in range(count):
            psswrd = psswrd+(random.choice(string.ascii_letters + string.digits))

        return psswrd

    def create_auctions(self,count):

        for i in range(1,count):
            seller=User.objects.get(username=self.usernames[random.randint(0,len(self.usernames)-1)])


            str_price = random.randint(1,70)
            item=self.items[random.randint(0,len(self.items)-1)]
            ending_time = (datetime.datetime.now()+datetime.timedelta(hours=75)).strftime('%Y-%m-%d %H:%M')
            print("User ", seller.username, " adds a auction for item ",item )
            Auction.objects.create(seller=seller, title='Selling a '+item, description='Old '+ item+' in good condition.', start_price=str_price,
                    latest_pid=str_price, auction_status='A', endtime=ending_time)

    def create_pids(self):
        auction_cnt=Auction.objects.count()
        num_of_pids=random.randint(1,10)+5
        pidder_cnt=User.objects.count()

        for i in range(num_of_pids):
            auction=Auction.objects.order_by('title')[random.randint(0,auction_cnt-1)]
            pidder = User.objects.order_by('username')[random.randint(0,pidder_cnt-1)]
            print("User ",pidder.username," adds a pid to auction ",auction.title)
            Pid.objects.create(auction_id=auction, pidder=pidder, pid_value=auction.latest_pid+random.randint(1,10),pid_datetime=datetime.datetime.now()+datetime.timedelta(hours=random.randint(1,7)))
