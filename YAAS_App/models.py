
from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin

from django.utils.translation import ugettext_lazy as _

from YAAS import settings


class Auction(models.Model):
    ACTIVE = 'A'
    BANNED = 'B'
    DUE = 'D'
    ADJUDICATED = 'E'
    AUCTION_STATUS = (
        (ACTIVE, 'Active'),
        (BANNED, 'Banned'),
        (DUE, 'Due'),
        (ADJUDICATED, 'Adjudicated')
    )
    # auction_id=models.AutoField(primary_key=True)
    seller = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    auction_status = models.CharField(max_length=1, default='A')
    description = models.TextField()
    start_price = models.DecimalField(max_digits=6, decimal_places=2)
    latest_bid = models.DecimalField(max_digits=6, decimal_places=2)
    endtime = models.DateTimeField()
    lockedby = models.TextField(default="#")

    # bidstatus
    def __str__(self):
        return self.title


class Bid(models.Model):
    # bid_id=models.AutoField(primary_key=True)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User)
    bid_value = models.DecimalField(max_digits=6, decimal_places=2)
    bid_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.auction_id) + ": " + str(self.bidder.username)


# class Profile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE) #blank=False
#     lang_preference = models.CharField(default='en', max_length=4, choices=settings.LANGUAGES)
#
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created: # and not kwargs.get('raw', False):
#             Profile.objects.create(user=instance)
#
#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.profile.save()
