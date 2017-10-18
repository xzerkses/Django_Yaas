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
    ACTIVE = 'A'
    BANNED = 'B'
    DUE ='D'
    ADJUDICATED ='E'
    AUCTION_STATUS = (
        (ACTIVE, 'Active'),
        (BANNED, 'Banned'),
        (DUE, 'Due'),
        (ADJUDICATED, 'Adjudicated')
    )
    #auction_id=models.AutoField(primary_key=True)
    seller=models.ForeignKey(User)
    title=models.CharField(max_length=100)
    auction_status=models.CharField(max_length=1,default='A')
    description=models.TextField()
    start_price=models.DecimalField(max_digits=6,decimal_places=2)
    latest_pid=models.DecimalField(max_digits=6,decimal_places=2)
    endtime=models.DateTimeField()

        #pidstatus
    def __str__(self):
        return self.title



class Pid(models.Model):
    #pid_id=models.AutoField(primary_key=True)
    auction_id=models.ForeignKey(Auction,on_delete=models.CASCADE)
    pidder=models.ForeignKey(User)
    pid_value=models.DecimalField(max_digits=6,decimal_places=2)
    pid_datetime=models.DateTimeField()

    def __str__(self):
        return str(self.auction_id) +": "+str(self.pidder.username)


