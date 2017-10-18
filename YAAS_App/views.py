from unicodedata import decimal

from decimal import Decimal
from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views import View
from _datetime import datetime
from YAAS_App.forms import CreateAuction, ConfirmAuction, RegistrationForm, AddPid, ConfirmBan
from YAAS_App.models import User, Auction, Pid
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
import requests
import re


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=True
            user.save()

            messages.add_message(request, messages.INFO, "New User is created. Please Login")

            return HttpResponseRedirect(reverse("home"))
        else:
            form = RegistrationForm(request.POST)
    else:
        print("not valid")
        form =RegistrationForm()

    return render(request, "registration/registration.html", {'form': form})


class EditNameView(View):
    def get(self, request, name):
        p = get_object_or_404(User, name=name)
        return render(request, "edit.html", {"name": p.name})

    def post(self, request, name):
        p = get_object_or_404(User, name=name)
        p.name = request.POST["name"]
        p.save()
        # Always redirect after a successful POST request
        return HttpResponseRedirect('/get/' + p.name)

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
            print(start_price)
            latest_pid=start_price #cleandata['latest_pid']
            print(latest_pid)
            endtime=cleandata['endtime']
            status=cleandata['auction_status']

            form=ConfirmAuction()
            endingdate = endtime.strftime('%Y-%m-%d %H:%M') # from datetime to string

            return render(request, 'confirmauction.html',
                          {'form':form,'seller':seller,'title':title,'description':description,
                           'start_price':start_price,'latest_pid':latest_pid,'endtime':endingdate,
                           'status':status})
        else:
            messages.add_message(request,messages.ERROR,"Data in form is not valid")
            return render(request,'createauction.html',{'form':form})

@login_required()
def saveauction(request):
    option = request.POST.get('option', '')

    if option == 'Yes':
        a_seller=request.user
        a_title = request.POST.get('title', '')

        a_description = request.POST.get('description', '')
        a_start_price = request.POST.get('start_price', '')
        a_latest_pid=request.POST.get('latest_pid','')
        tmp_end_time = request.POST.get('endtime', '')

        a_end_time=datetime.strptime(tmp_end_time,'%Y-%m-%d %H:%M') #'%Y-%m-%d %H:%M'

        auction = Auction(seller=a_seller,title =a_title, description = a_description, start_price=a_start_price,latest_pid=a_latest_pid, endtime=a_end_time)
        auction.save()
        sendAuctionEmail()
        return HttpResponseRedirect(reverse("home"))  #reverse(
    else:
        return HttpResponseRedirect(reverse("home"))

def browseauctions(request):

    auctions=Auction.objects.all().order_by('title')
    response = requests.get("http://api.fixer.io/latest")

    if not "sel_currency" in request.session:
        request.session["sel_currency"]="EUR"

    if not "rate" in request.session:
        request.session["rate"] = 1
    data=response.json()
    currency=request.session["sel_currency"]
    rate =request.session["rate"]
    rates = data['rates']

    return render(request, "auctionslist.html", {'auctions':auctions,'rates':rates,'currency':currency,'rate':rate})

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
        auction.save()
        messages.add_message(request,messages.INFO,"Auction successfully saved")
        return HttpResponseRedirect(reverse("home"))




@login_required
def editauction(request,offset):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s')
    else:
        auction=get_object_or_404(Auction, id=offset)
        if request.user==auction.seller:
            return render(request,"editauction.html",{'seller':request.user,'title':auction.title,
                                                      'description':auction.description,
                                                      'start_price':auction.start_price,
                                                      'endtime':auction.endtime,'id':auction.id})
        else:
            messages.add_message(request, messages.ERROR, "Only seller is allowed to edit auction")
            return HttpResponseRedirect(reverse("home"))
def search(request):
    #form=Searchingform()
    input=request.GET.get('query','')
    if input:
        input=input.strip()
        print(input)
        #form = Searchingform({'input':input})
        auctions=Auction.objects.filter(title__contains=input)[:10]
        print(auctions)
    else:
        auctions=[]

    return render(request,"searchauction.html",{'auctions': auctions,'input':input})

def sendemail():
    subject='Test notification'
    message='This a notification message as you have created a Auction to Old Junk Auctions site.'
    from_email='mkkvjk7@gmail.com'
    recipient_list='mkkvjk7@live.com'

    send_mail(subject, message, from_email,[recipient_list],fail_silently=False)

    return HttpResponseRedirect(reverse("home"))


def sendAuctionEmail():
    mail_subject = 'Notification from Old Junk Auctions.'
    user = User.objects.get(id=2)
    to_email = user.email
    message='You have created new auction in Old Junk Auctions site.'
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

def readJson(request):

    if request.method=='POST':
        selection = request.POST.get('dropdown','')
        value = re.split("\s", selection)
        curr = value[0]
        request.session["sel_currency"]=curr
        #print(curr)
        rate = value[1]
        request.session["rate"] = rate
        #print(rate)

    else:

        return redirect('/')

    return HttpResponseRedirect(reverse("home"))



@login_required
def addpid(request,offset):
    if request.method == 'GET':
        print("first step is ok")
        if not request.user.is_authenticated():
            messages.add_message(request, messages.ERROR, "You must login before you are allowed to pid")
            return HttpResponseRedirect('/login/?next=%s')
        else:
            auction = get_object_or_404(Auction, id=offset)
            #print("2nd step is ok")
            print(auction)
            print(auction.auction_status=='A')

            if not request.user.is_staff and (not request.user.username==auction.seller) and auction.auction_status=='A':
                form=AddPid()
                print("3rd step is ok")
                return render(request,'pid.html',{'form': form, 'auction':auction})
            else:
                if request.user.is_staff:
                    messages.add_message(request, messages.ERROR, "Administrators are not allowed to pid")
                if request.user.username==auction.seller:
                    messages.add_message(request, messages.ERROR, "Seller is not allowed to pid")
                return HttpResponseRedirect(reverse("home"))#if request.user == auction.seller:
    else:
        print("This is not GET method")
        return HttpResponseRedirect(reverse("home"))

def check_endingtime(end_datetime):
    dt = datetime.now().strftime('%Y-%m-%d %H:%M')
    dateobjnow = datetime.strptime(dt, '%Y-%m-%d %H:%M')
    endobj = end_datetime.strftime('%Y-%m-%d %H:%M')
    enddateobj = datetime.strptime(endobj, '%Y-%m-%d %H:%M')
    return enddateobj<dateobjnow



def savepid(request,offset):
    auction = get_object_or_404(Auction, id=offset)
    if request.method == "POST":
        form = AddPid(request.POST)
        latest_pid = request.POST["latest_pid"].strip()

        if form.is_valid():

            if not request.user.is_staff:

                cleandata = form.cleaned_data
                a_pid_value = cleandata["pid"]


                if a_pid_value < Decimal(latest_pid):
                    messages.add_message(request, messages.ERROR, "Pid value must be higher than previous pid.")
                    return render(request, 'pid.html', {'form': form, 'auction': auction})
                print(auction.endtime)
                print(datetime.now())
                if check_endingtime(auction.endtime):
                    messages.add_message(request, messages.ERROR, "Piding time has ended.")
                    auction.auction_status='C'
                    auction.save()
                    return render(request, 'pid.html', {'form': form, 'auction': auction})

                a_pidder=request.user

                a_pid_datetime=datetime.now()
                print(a_pid_value)


                pid = Pid(pidder=a_pidder,auction_id=auction, pid_value=a_pid_value,pid_datetime=a_pid_datetime)
                pid.save()

                auction.latest_pid=a_pid_value
                auction.save()
                messages.add_message(request, messages.INFO, "Pid successfully saved")

                mail_subject = "A new pid was placed in auction were you are involved."

                message = "New pid with " + str(a_pid_value) + " was placed on auction " + auction.title + ". Pidding is endind " + datetime.strftime(auction.endtime,'%Y-%m-%d %H:%M')

                pids = Pid.objects.filter(auction_id=auction).distinct()
                pidders = [p.pidder for p in pids]
                emails_addresses = list(set([p.email for p in pidders]))

                seller_email=(auction.seller).email
                emails_addresses.append(seller_email)
                to_email = emails_addresses

                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return HttpResponseRedirect(reverse("home"))

        else:

            messages.add_message(request, messages.ERROR, "Data in form is not valid")
            auction = Auction.objects.filter(id=offset)
            return render(request, 'pid.html', {'form': form,'auction':auction })

@login_required
def banview(request,offset):
    if request.method=='GET':
        if not request.user.is_authenticated() or not request.user.is_staff:
            messages.add_message(request, messages.ERROR, "You must login before you are allowed to ban")
            return HttpResponseRedirect('/login/?next=%s')
        else:
            auction=get_object_or_404(Auction,id=offset)
            print(auction.title)
            form=ConfirmBan()
            return render(request,'confirmban.html',{'auction':auction})

def ban(request,offset):
    option=request.POST.get('option','')
    if option=='Yes':
        auction = get_object_or_404(Auction, id=offset)
        auction.auction_status = 'B'
        print(auction.auction_status)
        auction.save()
        messages.add_message(request, messages.INFO, "Auction successfully banned")

        pids = Pid.objects.filter(auction_id=auction).distinct()
        pidders = [p.pidder for p in pids]
        emails_addresses = list(set([p.email for p in pidders]))

        seller_email = (auction.seller).email
        emails_addresses.append(seller_email)
        to_email = emails_addresses
        mail_subject="Auction "+str(auction.title)+" was banned by admin."
        message="Auction "+str(auction.title)+" was banned by administrator. Auction did not comply to rules of auction."
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return HttpResponseRedirect(reverse("home"))

    else:

        return HttpResponseRedirect(reverse("home"))







