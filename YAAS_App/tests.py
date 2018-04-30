import datetime

from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser
from django.core import mail
from django.test import TestCase, RequestFactory
from django.test import Client
from YAAS_App.models import Auction, Bid
from YAAS_App.views import saveauction
from _datetime import datetime, timedelta


class AuctionTestCases(TestCase):

    fixtures =['db_data.json']
    def setUp(self):

        #self.user =User.objects.create_user(username='alf', email='alf@trader.fi', password='alf123')
        self.user=User.objects.get(username='alf')
        response = self.client.login(username='alf', password='alf123')

    def test_redict_createauction(self):
        #
        response = self.client.get('/createauction/',follow=True)
        self.assertEqual(response.status_code, 200)

    def test_create_auction_db_level(self):
        # Creating seller for auction and adding auction to database
        auction_count=Auction.objects.count()
        endtime = datetime.now() + timedelta(days=4)
        Auction.objects.create(seller=self.user,title='Old Hammer',auction_status='A',
                               description='Rusty Hammer for sale',start_price=5.0,latest_bid=5.0,
                               endtime=datetime.strftime(endtime, '%Y-%m-%d %H:%M'))
        self.assertEqual(auction_count+1,Auction.objects.count())


    def test_create_auction_form_POST_too_short_auction_time(self):
        #self.client.login(username='alf', password='alf123')
        endtime=datetime.now()+timedelta(days=2)

        response=self.client.post('/createauction/', {'ShortTime': 'A Stone Statue',
                                           'description': 'Fine stone statue for sale', 'start_price': 15.0,'latest_bid': 15.0,
                                           'auction_status':'A','endtime': datetime.strftime(endtime, '%Y-%m-%d %H:%M')},follow=True)
        m = list(response.context['messages'])
        #print(str(m[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(m[0]), "Data in form is not valid.")

    def test_create_auction_form_POST_wrong_time_format_entered(self):
        #self.client.login(username='alf', password='alf123')
        endtime=datetime.now()+timedelta(days=2)

        response=self.client.post('/createauction/', {'title': 'A Stone Statue',
                                           'description': 'Fine stone statue for sale', 'start_price': 15.0,'latest_bid': 15.0,
                                           'auction_status':'A','endtime': datetime.strftime(endtime, '%Y-%m-%d %H')},follow=True)
        m = list(response.context['messages'])
        print(str(m[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(m[0]), "Data in form is not valid.")


    def test_create_auction_form_POST_too_low_auction_price(self):
        #self.client.login(username='alf', password='alf123')
        endtime=datetime.now()+timedelta(days=4)

        response=self.client.post('/createauction/', {'title': 'A Stone Statue',
                                           'description': 'Fine stone statue for sale', 'start_price': 0.005,'latest_bid': 0.005,
                                           'auction_status':'A','endtime': datetime.strftime(endtime, '%Y-%m-%d %H:%M')},follow=True)
        m = list(response.context['messages'])
        #print(str(m[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(m[0]), "Data in form is not valid.")

    def test_create_auction_form_POST_no_title(self):
        #self.client.login(username='alf', password='alf123')
        endtime=datetime.now()+timedelta(days=4)

        response=self.client.post('/createauction/', {'title': '',
                                           'description': 'Fine stone statue for sale', 'start_price': 0.005,'latest_bid': 0.005,
                                           'auction_status':'A','endtime': datetime.strftime(endtime, '%Y-%m-%d %H:%M')},follow=True)
        m = list(response.context['messages'])
        #print(str(m[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(m[0]), "Data in form is not valid.")

    def test_create_auction_form_POST_no_title(self):
        #self.client.login(username='alf', password='alf123')
        endtime=datetime.now()+timedelta(days=4)

        response=self.client.post('/createauction/', {'title': '',
                                           'description': 'Fine stone statue for sale', 'start_price': 0.005,'latest_bid': 0.005,
                                           'auction_status':'A','endtime': datetime.strftime(endtime, '%Y-%m-%d %H:%M')},follow=True)
        m = list(response.context['messages'])
        #print(str(m[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(m[0]), "Data in form is not valid.")

    def test_create_auction_form_POST_no_description(self):
        # self.client.login(username='alf', password='alf123')
        endtime = datetime.now() + timedelta(days=4)

        response = self.client.post('/createauction/', {'title': 'A Stone Statue',
                                                        'description': '',
                                                        'start_price': 0.005, 'latest_bid': 0.005,
                                                        'auction_status': 'A',
                                                        'endtime': datetime.strftime(endtime, '%Y-%m-%d %H:%M')}, follow=True)
        m = list(response.context['messages'])
        print(str(m[0]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(m[0]), "Data in form is not valid.")



    def test_save_auction_with_POST(self):
        auction_count=Auction.objects.count()
        # print("Test 4: START***********************************************************************************")
        # print("A number of auctions in the database now:", Auction.objects.count())
        endtime=datetime.now()+timedelta(days=4)

        response=self.client.post('/saveauction/', {'option':'Yes', 'seller': self.user, 'title': 'A Stone Statue',
                                           'description': 'Fine statue for sale', 'start_price': 15.0,'latest_bid': 15.0,
                                           'auction_status':'A','endtime': datetime.strftime(endtime, '%Y-%m-%d %H:%M')})
        #print("auctions after post",Auction.objects.count())
        self.assertEqual(auction_count + 1, Auction.objects.count())
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response, '/')



    def test_save_auction_with_POST_option_is_no(self):
        auction_count=Auction.objects.count()
        # print("Test 4: START***********************************************************************************")
        # print("A number of auctions in the database now:", Auction.objects.count())
        endtime=datetime.now()+timedelta(days=4)

        response=self.client.post('/saveauction/', {'option':'No', 'seller': self.user, 'title': 'A Stone Statue',
                                           'description': 'Fine statue for sale', 'start_price': 15.0,'latest_bid': 15.0,
                                           'auction_status':'A','endtime': datetime.strftime(endtime, '%Y-%m-%d %H:%M')})
        #print("auctions after post",Auction.objects.count())
        self.assertEqual(auction_count , Auction.objects.count())
        self.assertEqual(len(mail.outbox), 0)
        self.assertRedirects(response, '/')

    def test_add_auction_not_authenticated(self):

        # test createauction without logged in user
        self.client.logout()
        response = self.client.get('/createauction/',follow=True)
        #print("redirection :",response.redirect_chain)
        last_url, status_code = response.redirect_chain[0]
        #print("last url", last_url)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response,'/login/?next=/createauction/')
        #print("Test 5: *************************************************************************************END")


class BidTestCases(TestCase):
    fixtures = ['db_data.json']
    def setUp(self):
        self.user = User.objects.get(username='alf')
        self.seller = User.objects.get(username='seller')
        #login user in
        testtime=datetime.now()+timedelta(days=4)
        self.auction = Auction.objects.create(seller=self.seller, title='Old Sledgehammer', auction_status='A',
                                             description='Rusty Sledgehammer for sale', start_price=5.0, latest_bid=5.0,
                                             endtime=datetime.strftime(testtime,'%Y-%m-%d %H:%M'))

        self.auction.save()
        testtime_minutes = datetime.now() + timedelta(minutes=4)
        self.auction_ending = Auction.objects.create(seller=self.seller, title='Old Sledgehammer', auction_status='A',
                                              description='Rusty Sledgehammer for sale', start_price=5.0,
                                              latest_bid=5.0,
                                              endtime=datetime.strftime(testtime_minutes, '%Y-%m-%d %H:%M'))
        self.auction_ending.save()

        testtime_ended= datetime.now() - timedelta(minutes=20)
        self.auction_ended = Auction.objects.create(seller=self.seller, title='Old Sledgehammer', auction_status='A',
                                                     description='Rusty Sledgehammer for sale', start_price=5.0,
                                                     latest_bid=5.0,
                                                     endtime=datetime.strftime(testtime_ended, '%Y-%m-%d %H:%M'))
        self.auction_ended.save()
        response = self.client.login(username='alf', password='alf123')

    def test_addbid(self):
        bid_value=5.5 #self.auction.latest_bid+0.1
        bid_count=Bid.objects.count()
        response=self.client.post('/savebid/'+str(self.auction.pk),{'bid':bid_value,'auction_id':self.auction,'latest_bid':self.auction.latest_bid, 'description':'', 'endtime':''})
        self.assertEqual(bid_count + 1, Bid.objects.count())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(response.status_code, 302)

    def test_addbid_too_low_bid(self):
        pid_value = 5.0
        bid_count = Bid.objects.count()
        #print("pid_val: ", self.auction.latest_bid)
        response = self.client.post('/savebid/' + str(self.auction.pk),
                                    {'bid': pid_value, 'auction_id': self.auction,
                                     'latest_bid': self.auction.latest_bid,
                                     'description': '', 'endtime': ''})
        m = list(response.context['messages'])
        #print("msg 0: ",str(m[0]))
        self.assertEqual(bid_count, Bid.objects.count()) #"bid value must be at least 0.01 higher than previous bid."
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(m[0]), "bid value must be at least 0.01 higher than previous bid.")

    def test_addbid_bidding_ending(self):
        pid_value = 5.6
        bid_count = Bid.objects.count()
        # print("pid_val: ", self.auction.latest_bid)
        org_ending=self.auction_ending.endtime

        print("Testing time ", org_ending)
        response = self.client.post('/savebid/' + str(self.auction_ending.pk),
                                    {'bid': pid_value, 'auction_id': self.auction_ending,
                                     'latest_bid': self.auction_ending.latest_bid,
                                     'description': '', 'endtime': ''})

        self.assertEqual(bid_count+1,
                         Bid.objects.count())  # "bid value must be at least 0.01 higher than previous bid."
        time_now=datetime.now()

        self.assertGreater(org_ending, datetime.strftime(time_now, '%Y-%m-%d %H:%M'))
        self.assertEqual(org_ending, self.auction_ending.endtime)
        self.assertEqual(response.status_code, 302)

    def test_addbid_bidding_already_ended(self):
        #self.auction_ending.auction_status='C'
        pid_value = 5.6
        bid_count = Bid.objects.count()
        #print("auction_status: ", self.auction_ended.auction_status)
        org_ending = self.auction_ended.endtime

        #print("Testing time ", org_ending)
        response = self.client.post('/savebid/' + str(self.auction_ended.pk),
                                    {'bid': pid_value, 'auction_id': self.auction_ended,
                                     'latest_bid': self.auction_ended.latest_bid,
                                     'description': '', 'endtime': ''})

        self.assertEqual(bid_count ,
                         Bid.objects.count())
        m = list(response.context['messages'])
        #print("message: ",str(m[0]))
        self.assertEqual(str(m[0]),"biding time has ended.")
        self.assertEqual(response.status_code, 200)

    def test_addbid_seller_adds_bid_to_own_auction(self):
        self.client.logout()
        self.client.login(username='seller', password='sel56')
        user=auth.get_user(self.client)
        response = self.client.get('/addbid/' + str(self.auction.pk),follow=True)
        m = list(response.context['messages'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(m[0]), "Seller is not allowed to bid")
        self.assertRedirects(response, '/')

    def test_addbid_user_adds_bid_to_auction(self):

        self.client.logout()
        self.client.login(username='alf',email='alf@trader.fi', password='alf123')
        user = auth.get_user(self.client)
        response = self.client.get('/addbid/' + str(self.auction.pk),follow=True)
        self.assertEqual(response.status_code, 200)

class ConcurrencyTestCases(TestCase):

    fixtures = ['db_data.json']

    @classmethod
    def setUp(self):

        self.auction_count = Auction.objects.count()
        endtime = datetime.now()+timedelta(days=4)
        self.seller = User.objects.get(username='seller')
        self.auction = Auction.objects.create(seller=self.seller, title='Old Sledgehammer', auction_status='A',
                                             description='Rusty Sledgehammer for sale', start_price=5.0, latest_bid=5.0,
                                             endtime=datetime.strftime(endtime, '%Y-%m-%d %H:%M'))
        self.auction.lockedby = "test"
        self.auction.save()
        #self.tester = User.objects.create_user(username='tester', email='tester@testing.fi', password='tester123')
        self.tester = User.objects.get(username='alf')
        #changing auction lockedby status
        print("Locked by status:",self.auction.lockedby)


    def test_adding_bid_when_auction_is_locked(self):
        # adding test user
        response = self.client.login(username='alf', password='alf123')
        test=Auction.objects.get(title='Old Sledgehammer')
        response = self.client.get('/addbid/'+str(test.id),follow=True)

        msg = list(response.context['messages'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(msg[0]), "Someone else is currently accessing auction data. Try again a bit later.")
        self.assertRedirects(response, '/')

    def test_editauction_when_auction_is_locked(self):
        # addinf test user
        response = self.client.login(username='seller', password='sel56')
        test = Auction.objects.get(title='Old Sledgehammer')
        response=self.client.get('/editauction/' + str(test.id),follow=True)
        msg = list(response.context['messages'])
        print("msg: ", str(msg[0]))
        self.assertEqual(str(msg[0]), "Auction is currently used by another user. You can try to edit auction later.")
        #self.assertRedirects(response, '/')

    def test_banauction_when_auction_is_locked(self):
        # addinf test user
        response = self.client.login(username='seller', password='sel56')
        test = Auction.objects.get(title='Old Sledgehammer')
        response=self.client.get('/banview/' + str(test.id),follow=True)
        print(response)
        msg = list(response.context['messages'])

        self.assertEqual(str(msg[0]), "Someone else is currently accessing auction data. Try again a bit later.")
        self.assertEquals(response.status_code, 200)