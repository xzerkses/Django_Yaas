
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
from YAAS_App.forms import CreateAuction, ConfirmAuction, Searchingform, RegistrationForm
from YAAS_App.models import User, Auction
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
import requests
import json
import urllib3

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()

            messages.add_message(request, messages.INFO, "New User is created. Please Login")

            return HttpResponseRedirect(reverse("home"))
        else:
            form = UserCreationForm(request.POST)
    else:
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
            endtime=cleandata['endtime']

            form=ConfirmAuction()
            endingdate = endtime.strftime('%Y-%m-%d %H:%M') # from datetime to string

            return render(request, 'confirmauction.html',
                          {'form':form,'seller':seller,'title':title,'description':description,
                           'start_price':start_price,'endtime':endingdate})
        else:
            messages.add_message(request,messages.ERROR,"Data in form is not valid")
            return render(request,'createauction.html',{'form':form,})
@login_required()
def saveauction(request):
    option = request.POST.get('option', '')

    if option == 'Yes':
        a_seller=request.user
        a_title = request.POST.get('title', '')

        a_description = request.POST.get('description', '')
        a_start_price = request.POST.get('start_price', '')
        tmp_end_time = request.POST.get('endtime', '')

        a_end_time=datetime.strptime(tmp_end_time,'%Y-%m-%d %H:%M') #'%Y-%m-%d %H:%M'

        auction = Auction(seller=a_seller,title =a_title, description = a_description, start_price=a_start_price, endtime=a_end_time)
        auction.save()
        sendAuctionEmail()
        return HttpResponseRedirect(reverse("home"))  #reverse(
    else:
        return HttpResponseRedirect(reverse("home"))

def browseauctions(request):

    auctions=Auction.objects.all().order_by('title')
    #auctions=Auction.objects.order_by('-endtime')
    response = requests.get("http://api.fixer.io/latest")
    data=response.json()
    rates = data['rates']
    return render(request, "auctions.html", {'auctions':auctions,'rates':rates})

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
                                                      'endtime':auction.endtime})

def search(request):
    form=Searchingform()
    query=request.GET.get('q','')
    if query:
        query=query.strip()
        form = Searchingform({'query':query})
        auctions=Auction.objects.filter(title__icontains=query)[:10]
    else:
        auctions=[]

    return render(request,"searchauction.html",{'auctions': auctions,'query':query})

def sendemail():
    subject='Test notification'
    message='This a notification message as you have created a Auction to Old Junk Auctions site.'
    from_email='mkkvjk7@gmail.com'
    recipient_list='mkkvjk7@live.com'

    send_mail(subject, message, from_email,[recipient_list],fail_silently=False)
    # return HttpResponse('Email sent')
    return HttpResponseRedirect(reverse("home"))


def sendAuctionEmail():
    mail_subject = 'Notification from Old Junk Auctions.'
    user = User.objects.get(id=2)
    to_email = user.email
    message='You have created new auction in Old Junk Auctions site.'
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()

def readJson(request):
    #response = requests.get("http://api.fixer.io/latest")
    print("täällä")
    #rates={'eka':2,'toka':3,'kolmas':4}
    selection=requests.POST.get('dropdown')
    if request.method=='GET':
        print("ollaankin täällä")
    else:

        print("löytyi")
        return redirect('/home/')
    #return render(request,'base.html',{'form':form})
    #base=data['base']
    #response=
    #date=data['date']
    #rates=data['rates']
    #messages.add_message(request, messages.INFO, "Json data read")
    return HttpResponseRedirect(reverse("home"))
