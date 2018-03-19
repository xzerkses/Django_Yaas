import datetime

from django.contrib.auth.models import User, AnonymousUser
from django.core import mail
from django.test import TestCase, RequestFactory

from YAAS_App.models import Auction, Pid
from YAAS_App.views import saveauction


class AuctionTestCases(TestCase):
    fixtures = ['db_data.json']
    def setUp(self):
        print("Test init: START***********************************************************************************")
        print("A number of users in database is now: ",User.objects.count())
        self.user =User.objects.create_user(username='alf', email='alf@trader.fi', password='alf123')

        print("Added username",self.user,"to database. A number of users in database is now: ", User.objects.count())
        response = self.client.login(username='alf', password='alf123')
        print("Test init: *************************************************************************************END")

    def test_redict_createauction(self):
        print("Test 2: START***********************************************************************************")
        #test that create auction page responds
        response = self.client.get('/createauction/')
        self.assertEqual(response.status_code, 200)
        print("Test 2: *************************************************************************************END")


    def test_create_auction_db_level(self):
        # Creating seller for auction and adding auction to database
        auction_count=Auction.objects.count()
        print("Test 3: START***********************************************************************************")
        print("A number of auctions in the database before adding more auctions:",auction_count)
        Auction.objects.create(seller=self.user,title='Old Hammer',auction_status='A',
                               description='Rusty Hammer for sale',start_price=5.0,latest_pid=5.0,
                               endtime='2018-04-27 18:00')
        self.assertEqual(auction_count+1,Auction.objects.count())
        print("A number of auctions in the database now:", Auction.objects.count())
        print("Test 3: *************************************************************************************END")

    def test_create_auction(self):
        auction_count=Auction.objects.count()
        print("Test 4: START***********************************************************************************")
        print("A number of auctions in the database now:", Auction.objects.count())
        response=self.client.post('/saveauction/', {'option':'Yes', 'seller': self.user, 'title': 'A Stone Statue',
                                           'description': 'Fine statue for sale', 'start_price': 15.0,'latest_pid': 15.0,
                                           'auction_status':'A','endtime': '2018-04-27 18:00'})
        print("auctions after post",Auction.objects.count())
        self.assertEqual(auction_count + 1, Auction.objects.count())
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response, '/')
        print("Test 4: ********************************************************************************************END")

    def test_reset_user(self):
        #change anonymous user
        self.user=AnonymousUser()
        response = self.client.login(response = self.client.login(username=' ', password=' '))
        self.failUnlessEqual(response,False)

    def test_add_auction(self):
        print("Test 5: START***********************************************************************************")
        print("Testing that user authentication works")
        # test that create auction page responds
        response = self.client.get('/createauction/')
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response,'login/')
        print("Test 5: *************************************************************************************END")


class SimpleTestWithFactory(TestCase):
    fixtures = ['db_data.json']
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = self.user =User.objects.create_user(username='alf',
                                                        email='alf@trader.fi', password='alf123')
    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/saveauction/')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.

        # request=self.client.post('/saveauction/', {'seller': self.user, 'title':'A Stone Statue','auction_status': 'A'
        #     ,'description':'Fine statue for sale','start_price':15.0,'latest_pid':15.0,
        #                                              'endtime':datetime.datetime.now()+datetime.timedelta(4)})
        request = self.factory.post('/saveauction/', {'option':'Yes', 'seller': self.user, 'title': 'A Stone Statue',
                                           'description': 'Fine statue for sale', 'start_price': 15.0,'latest_pid': 15.0,
                                           'auction_status':'A','endtime': datetime.datetime.now() + datetime.timedelta(4)})

class PidTestCases(TestCase):
    fixtures = ['db_data.json']
    def setUp(self):
        # Every test needs access to the request factory.
        self.user = self.user = User.objects.create_user(username='alf',email='alf@trader.fi', password='alf123')
        #login user in
        response = self.client.login(username='alf', password='alf123')

    def test_addpid(self):
        self.client.post('/savepid/',{})

    # < label > < b > Title: < / b > {{auction.title}} < / label > < br >
    # < label > < b > Description: < / b > {{auction.description}} < / label > < br >
    # < label > < b > Auction
    # Status: < / b > {{auction.auction_status}} < / label > < br >
    # < label > < b > Starting
    # pid: < / b > {{auction.start_price}} < / label > < br >
    # < label > < b > Latest
    # Pid: < / b > {{auction.latest_pid}} < / label > < br >
    #
    # {{form.as_p}}
    # < INPUT
    # TYPE = HIDDEN
    # NAME = "auction_id"
    # VALUE = "{{auction.id}}" >
    # < INPUT
    # TYPE = HIDDEN
    # NAME = "latest_pid"
    # VALUE = "{{ auction.latest_pid }}" >
    # < INPUT
    # TYPE = HIDDEN
    # NAME = "description"
    # VALUE = "{{ description }}" >
    # < INPUT
    # TYPE = HIDDEN
    # NAME = "start_price"
    # VALUE = "{{ start_price }}" >
    # < INPUT
    # TYPE = HIDDEN
    # NAME = "endtime"
    # VALUE = "{{ endtime }}" >
