from datetime import datetime,timedelta

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
#from YAAS_App.myvalidators import validate_endtime
from django import forms
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from YAAS_App.models import Auction


def validate_endtime(end_date):
    dt = datetime.now().strftime('%Y-%m-%d %H:%M')
    dateobjnow = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    endobj=end_date.strftime('%Y-%m-%d %H:%M')
    enddateobj = datetime.strptime(endobj,'%Y-%m-%d %H:%M')
    delta=enddateobj-dateobjnow
    if (delta<timedelta(hours=72)):
        raise ValidationError(' Pidding time must be longer than 72 hours.')

def validate_pidtime(end_datetime):
    if datetime.now()>end_datetime:
        raise ValidationError('Pidding not possible anymore. Pidding ended.')




def validate_status(value):
    if not value == 'A':
        raise ValidationError(('pidding not possible anymore. Auction is not active anymore.'),
                              params={'value': value})



class CreateAuction(forms.Form):
    title=forms.CharField(required=True,)#validators=[validate_test])
    description=forms.CharField(widget=forms.Textarea(),required=True)
    auction_status=forms.CharField(initial=Auction.ACTIVE,validators=[validate_status],widget=forms.HiddenInput())
    start_price=forms.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(0.01)])
    endtime=forms.DateTimeField(required=True,validators=[validate_endtime],help_text="Please use the following format: <em>YYYY-mm-dd HH:MM</em>.")

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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

