from datetime import datetime,timedelta


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
#from YAAS_App.myvalidators import validate_endtime
from django import forms
from django.core.validators import MinValueValidator
from django.utils import timezone

from YAAS_App.models import Auction


def validate_endtime(endate):
    dt = datetime.now().strftime('%Y-%m-%d %H:%M')
    dateobjnow = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    dtstr=endate-dateobjnow
    print(dtstr)
    if (dtstr<timedelta(hours=72)):
        raise ValidationError(('%endate) pidding time must be longer than 72 hours'),
                              params={'endate':endate},)

def validate_status(value):
    if not value == 'A':
        raise ValidationError(('pidding not possible anymore. Auction is not active anymore'),
                              params={'value': value})

#def validate_status(auction_status):
 #   if not auction_status=='active':
        #raise ValidationError(('%auction_status) Pidding not possible. Auction is not active anymore'),
         #                     params={'auction_status': auction_status} )

def validate_test(value):
    print("we are here")
    print(value)

class CreateAuction(forms.Form):
    title=forms.CharField(required=True,validators=[validate_test])
    description=forms.CharField(widget=forms.Textarea(),required=True)
    auction_status=forms.CharField(initial=Auction.ACTIVE,validators=[validate_status])#,widget=forms.HiddenInput()
    start_price=forms.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(0.01)])
    endtime=forms.DateTimeField(required=True,help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

class AddPid(forms.Form):
    pid=forms.DecimalField(required=True,max_digits=6,decimal_places=2,validators=[])


class ConfirmAuction(forms.Form):
    CHOICES = [(x, x) for x in ("Yes", "No")]
    option = forms.ChoiceField(choices=CHOICES, required=True,initial='Yes')
    t_title = forms.CharField(widget=forms.HiddenInput())

class ConfirmBan(forms.Form):
    CHOICES = [(x, x) for x in ("Yes", "No")]
    option = forms.ChoiceField(choices=CHOICES, required=True,initial='Yes')
    t_title = forms.CharField(widget=forms.HiddenInput())

class RegistrationForm(UserCreationForm):
    email=forms.EmailField(label='Email',max_length=200,help_text='Required')
    class Meta:
        model=User
        fields =('username','email','password1','password2')



