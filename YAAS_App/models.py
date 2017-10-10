from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _



class Auction(models.Model):
    auction_id=models.AutoField(primary_key=True)
    seller=models.ForeignKey(User, related_name="seller")
    title=models.CharField(max_length=100)
    description=models.TextField()
    start_price=models.DecimalField(max_digits=6,decimal_places=2)
    endtime=models.DateTimeField()

    def __unicode__(self):
        return self.title

# class Pid(models.Model):
#     pid_id=models.AutoField(primary_key=True)
#     auction=models.ForeignKey(Auction)
#     pidder=models.ForeignKey(User)
#     pid_value=models.DecimalField(max_digits=6,decimal_places=2)
#     pid_datetime=models.DateTimeField()