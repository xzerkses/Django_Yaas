
from decimal import Decimal
from email.mime.multipart import MIMEMultipart

from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, request
from django.contrib.auth.decorators import login_required


from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views import View
from _datetime import datetime, timedelta
from YAAS_App.forms import CreateAuction, ConfirmAuction, RegistrationForm, AddBid, ConfirmBan, EditUserDataForm
from YAAS_App.models import User, Auction, Bid #Profile
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
import requests
import re


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=True
            user.save()

            messages.add_message(request, messages.INFO, _("New User is created. Please Login."))

            return HttpResponseRedirect(reverse("home"))
        else:
            form = RegistrationForm(request.POST)
    else:
        print("not valid")
        form =RegistrationForm()

    return render(request, "registration/registration.html", {'form': form})


@method_decorator(login_required, name="dispatch")
class AddAuction(View):

    def get(self, request):
        form=CreateAuction()
        return render(request,'createauction.html',{'form':form})

    def post(self, request):
        form=CreateAuction(request.POST)
        if form.is_valid():
            cleandata=form.cleaned_data
            seller=request.user.username
            title=cleandata['title']
            description=cleandata['description']
            start_price=cleandata['start_price']
            latest_bid=start_price
            endtime=cleandata['endtime']
            auction_status=cleandata['auction_status']

            form=ConfirmAuction()
            endingdate = endtime.strftime('%Y-%m-%d %H:%M') # from datetime to string

            return render(request, 'confirmauction.html',
                          {'form':form,'seller':seller,'title':title,'description':description,
                           'start_price':start_price,'latest_bid':latest_bid,'endtime':endingdate,
                           'auction_status':auction_status})
        else:
            messages.add_message(request,messages.ERROR,_("Data in form is not valid."))
            return render(request,'createauction.html',{'form':form})

@login_required()
def saveauction(request):
    option = request.POST.get('option', '')

    if option == 'Yes':
        a_seller=request.user
        a_title = request.POST.get('title', '')

        a_description = request.POST.get('description', '')
        a_start_price = request.POST.get('start_price', '')
        a_latest_bid=request.POST.get('latest_bid','')
        tmp_end_time = request.POST.get('endtime', '')

        a_end_time=datetime.strptime(tmp_end_time,'%Y-%m-%d %H:%M') #'%Y-%m-%d %H:%M'

        auction = Auction(seller=a_seller,title =a_title, description = a_description, start_price=a_start_price,latest_bid=a_latest_bid, endtime=a_end_time)
        auction.save()

        subject = _('Notification from Old Junk Auctions.')
        body=_('You have created a new auction in Old Junk Auctions site.')
        html_msg='<a href="http://127.0.0.1:8000/">Check added Auction</a>'
        to=request.user.email
        msg=EmailMultiAlternatives(subject, body, request.user.email, [to])
        msg.attach_alternative(html_msg,"text/html")

        msg.send()
        return HttpResponseRedirect(reverse("home"))  #reverse(
    else:
        return HttpResponseRedirect(reverse("home"))

def browseauctions(request):
    languages={'English':'en','German':'de','France':'fr'}
    auctions=Auction.objects.all().order_by('title')

    response = requests.get("http://api.fixer.io/latest")

    if not "sel_currency" in request.session:
        request.session["sel_currency"]="EUR"

    if not "rate" in request.session:
        request.session["rate"] = 1

    # if request.user.is_authenticated:
    #     if not request.user.profile.lang_preference:
    #         request.session[translation.LANGUAGE_SESSION_KEY] = "en"
    #         request.user.profile.lang_preference = "en"
    #         request.user.save()
    #         translation.activate("en")
    #
    #     else:
    #         lang = request.user.profile.lang_preference
    #         translation.activate(lang)
    #         request.session[translation.LANGUAGE_SESSION_KEY]=lang

    if not translation.LANGUAGE_SESSION_KEY in request.session:
        request.session[translation.LANGUAGE_SESSION_KEY] = 'en'
        translation.activate("en")

    data=response.json()
    currency=request.session["sel_currency"]
    rate =request.session["rate"]
    rates = data['rates']



    lang_type=request.session[translation.LANGUAGE_SESSION_KEY]

    for key, value in languages.items():
        if value == lang_type:
            language=key

    return render(request, "auctionslist.html", {'auctions':auctions,'rates':rates,'currency':currency,'rate':rate,'languages':languages,'language':language })

def savechanges(request,offset):
    auctions=Auction.objects.filter(id=offset)
    if len(auctions)> 0:
        auction=auctions[0]
    else:
        messages.add_message(request,messages.INFO,"Wrong auction id")
        return HttpResponseRedirect(reverse("home"))

    if request.method=="POST":
        description = request.POST["description"].strip()
        title = request.POST["title"].strip()
        auction.title=title
        auction.description=description
        auction.lockedby="#"
        #print("edited auction savad: ",auction.lockedby)
        auction.save()
        messages.add_message(request,messages.INFO,_("Auction successfully saved."))
        return HttpResponseRedirect(reverse("home"))


@login_required
def editauction(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s')
    else:
        auction=get_object_or_404(Auction, id=offset)
        if request.user==auction.seller:

            if auction.lockedby!="#" and auction.lockedby!=request.session._get_or_create_session_key():
                messages.add_message(request, messages.ERROR, _("Auction is currently used by another user. You can try to edit auction later."))
                return HttpResponseRedirect(reverse("home"))
            auction.lockedby=request.session._get_or_create_session_key()
            #print("auction locked for edit by: ",auction.lockedby)
            auction.save()
            return render(request,"editauction.html",{'seller':request.user,'title':auction.title,
                                                      'description':auction.description,
                                                      'start_price':auction.start_price,
                                                      'endtime':auction.endtime,'id':auction.id})
        else:
            messages.add_message(request, messages.ERROR, _("Only seller is allowed to edit auction."))
            return HttpResponseRedirect(reverse("home"))
def search(request):

    input=request.GET.get('query','')
    if input:
        input=input.strip()
        auctions=Auction.objects.filter(title__contains=input)[:10]

    else:
        auctions=[]

    return render(request,"searchauction.html",{'auctions': auctions,'input':input})


def sendEmail(subject, body, receivers):
    mail_subject = subject
    to_email = receivers
    message=body
    email = EmailMessage(mail_subject, message, to=[to_email])

    email.send()

def readJson(request):

    if request.method=='POST':
        selection = request.POST.get('dropdown','')
        value = re.split("\s", selection)
        curr = value[0]
        request.session["sel_currency"]=curr
        rate = value[1]
        request.session["rate"] = rate
    else:

        return redirect('/')

    return HttpResponseRedirect(reverse("home"))



@login_required
def addbid(request,offset):

    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, _("You must login before you are allowed to bid"))
        return HttpResponseRedirect('/login/?next=%s')
    else:
        auction = get_object_or_404(Auction, id=offset)

        if not request.user.is_staff and not (request.user.username==str(auction.seller)) and auction.auction_status=='A' and (auction.lockedby=="#" or auction.lockedby==request.session._get_or_create_session_key()):
            form=AddBid()
            auction.lockedby=request.session._get_or_create_session_key()

            auction.save()
            return render(request,'bid.html',{'form': form, 'auction':auction})
        else:
            if request.user.is_staff:
                messages.add_message(request, messages.ERROR, _("Administrators are not allowed to bid"))
            if request.user.username==str(auction.seller):
                print("Seller is here")
                messages.add_message(request, messages.ERROR, _("Seller is not allowed to bid"))
            if auction.lockedby!="#" and auction.lockedby!=request.session._get_or_create_session_key():
                messages.add_message(request, messages.ERROR, _("Someone else is currently accessing auction data. Try again a bit later."))


            return HttpResponseRedirect(reverse("home"))

def check_endingtime(end_datetime):
    dt = datetime.now().strftime('%Y-%m-%d %H:%M')
    dateobjnow = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    endobj = end_datetime.strftime('%Y-%m-%d %H:%M')
    enddateobj = datetime.strptime(endobj, '%Y-%m-%d %H:%M')
    return enddateobj<dateobjnow



def savebid(request,offset):
    auction = get_object_or_404(Auction, id=offset)
    if request.method == "POST":
        form = AddBid(request.POST)
        latest_bid = request.POST["latest_bid"].strip()

        if form.is_valid():

            if not request.user.is_staff:

                cleandata = form.cleaned_data
                a_bid_value = cleandata["bid"]


                if Decimal(a_bid_value) < Decimal(0.01)+Decimal(latest_bid):
                    messages.add_message(request, messages.ERROR, _("bid value must be at least 0.01 higher than previous bid."))
                    return render(request, 'bid.html', {'form': form, 'auction': auction})

                if(check_endingtime(auction.endtime-timedelta(minutes=5))):
                    auction.endtime=auction.endtime+timedelta(minutes=5)
                    auction.save()

                if check_endingtime(auction.endtime):
                    messages.add_message(request, messages.ERROR, _("biding time has ended."))
                    auction.auction_status='C'
                    auction.save()
                    return render(request, 'bid.html', {'form': form, 'auction': auction})

                a_bidder=request.user

                a_bid_datetime=datetime.now()
                print(a_bid_value)


                bid = Bid(bidder=a_bidder,auction_id=auction, bid_value=a_bid_value,bid_datetime=a_bid_datetime)
                bid.save()

                auction.latest_bid=a_bid_value
                auction.lockedby="#"
                auction.save()
                messages.add_message(request, messages.INFO, _("bid successfully saved."))

                mail_subject = _("A new bid was placed in auction were you are involved.")
                msg = _("New bid with value of " + str(a_bid_value) + " was placed on auction " + auction.title + ". bidding is endind " + datetime.strftime(auction.endtime,'%Y-%m-%d %H:%M'))

                bids = Bid.objects.filter(auction_id=auction).distinct()
                bidders = [p.bidder for p in bids]
                emails_addresses = list(set([p.email for p in bidders]))
                emails_addresses.append((auction.seller).email)

                sendEmail(mail_subject, msg, emails_addresses)
                return HttpResponseRedirect(reverse("home"))

        else:

            messages.add_message(request, messages.ERROR, _("Data in form is not valid"))
            auction = Auction.objects.filter(id=offset)
            return render(request, 'bid.html', {'form': form,'auction':auction })

@login_required
def banview(request,offset):

    print("Sanity check1")
    if not request.user.is_authenticated() and not request.user.is_staff:
        # messages.add_message(request, messages.ERROR, _("You must login before you are allowed to ban"))
        return HttpResponseRedirect('/login/?next=%s')


    else:
        auction = get_object_or_404(Auction, id=offset)
        print("here:",auction.lockedby)
        print("testing:",auction.lockedby!="#" and auction.lockedby!=request.session._get_or_create_session_key())
        if auction.lockedby!="#" and auction.lockedby!=request.session._get_or_create_session_key():
            print("Sanity check")
            messages.add_message(request, messages.ERROR,_("Someone else is currently accessing auction data. Try again a bit later."))
            HttpResponseRedirect(reverse("home"))




        form=ConfirmBan()
        return render(request,'confirmban.html',{'auction':auction})

def ban(request,offset):
    option=request.POST.get('option','')
    if option=='Yes':
        auction = get_object_or_404(Auction, id=offset)
        auction.auction_status = 'B'

        auction.save()
        messages.add_message(request, messages.INFO, _("Auction successfully banned"))

        mail_subject=_("Auction "+str(auction.title)+" was banned by admin.")
        msg=_("Auction "+str(auction.title)+" was banned by administrator. Auction did not comply to rules of auction.")

        bids = Bid.objects.filter(auction_id=auction)
        bidders = [b.bidder for b in bids]
        emails_addresses = list(set([b.email for b in bidders]))
        emails_addresses.append((auction.seller).email)
        sendEmail(mail_subject, msg, emails_addresses)

        return HttpResponseRedirect(reverse("home"))

    else:

        return HttpResponseRedirect(reverse("home"))

@login_required()
def edituser(request):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, _("You must login before you are edit your data"))
        return HttpResponseRedirect('/login/?next=%s')
    else:
        if request.method=="GET":
            user=request.user
            email=request.user.email
            pword=request.user.password
            data={'pword':pword,'email':email}
            form=EditUserDataForm(data,initial=data)#EditUserDataForm
            return render(request,'edituserdata.html',{'form':form}) #,{'old_email':email}

        else:
            form=EditUserDataForm(data=request.POST,user=request.user)
            if form.is_valid():
                cleandata = form.cleaned_data

                email = cleandata["email"]

                request.user.email=email
                form.save()
                update_session_auth_hash(request, form.user )
                messages.add_message(request, messages.INFO, _("You data has been saved."))
            return redirect('home')




def set_lang(request):
    selection = request.POST.get('languages', '')
    value = re.split("\s", selection)
    language = value[0]
    lang_type = value[1]
    translation.activate(lang_type)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_type

    # if request.user.is_authenticated:
    #     user=request.user
    #     user.profile.lang_preference=lang_type
    #     user.save()
    return HttpResponseRedirect(reverse("home"))

def clearhome(request,offset):
    if offset!="":
        auction = get_object_or_404(Auction, id=offset)
        auction.lockedby = "#"
        auction.save()

    return HttpResponseRedirect(reverse("home"))