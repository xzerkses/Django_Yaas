from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views import View
from _datetime import datetime
from YAAS_App.forms import CreateAuction, ConfirmAuction, Searchingform
from YAAS_App.models import User, Auction
from django.contrib import messages
from django.core.mail import send_mail


def hello(request):
    return HttpResponse("Hello, you are at the polls.")
def create(request,name):
    p = User(name)
    p.save()
    return HttpResponse("Created: "+name)

def filterPerson(request,name):
    try:
        p = User.objects.filter(name__contains=name)
    except Exception:
        return HttpResponse("Not found")
    return render(request,"show.html", {"name": p.name, "id":p.id})

def getPerson(request,name):
    try:
        p = User.objects.get(name=name)
    except Exception:
        return HttpResponse("not found")
    return render(request,"show.html", {"name":p.name,"id":p.id})

def set_name(request,name):
    request.session["name"] = name
    return HttpResponse("Name is set.")

def get_name(request):
    return HttpResponse(request.session["name"])

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            messages.add_message(request, messages.INFO, "New User is created. Please Login")

            return HttpResponseRedirect(reverse("home"))
        else:
            form = UserCreationForm(request.POST)
    else:
        form =UserCreationForm()

    return render(request, "registration/registration.html", {'form': form})

#def login_view(request):
#   if request.method == 'POST':
#        username = request.POST.get('username', '')
#        password = request.POST.get('password', '')
#        nextTo = request.GET.get('next', reverse("home"))
#        user = auth.authenticate(username=username, password=password)

#        if user is not None and user.is_active:
#            auth.login(request,user)
#            print (user.password)
#            return HttpResponseRedirect(nextTo)

#    return render(request,"login.html")



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
            send_mail('subject', 'Notification from Old Junk Auctions',
                      'This a notification message as you have created a Auction to Old Junk Auctions site.',
                      'mkkvjk7@gmail.com',
                      ['mijukiv@utu.fi'],
                      fail_silently=False,
                      )
            return render(request, 'confirmauction.html',
                          {'form':form,'seller':seller,'title':title,'description':description,
                           'start_price':start_price,'endtime':endingdate})
        else:
            messages.add_message(request,messages.ERROR,"Data in form is not valid")
            return render(request,'createauction.html',{'form':form,})

def saveauction(request):
    option = request.POST.get('option', '')
    print(option)
    if option == 'Yes':
        a_seller=request.user
        a_title = request.POST.get('title', '')

        a_description = request.POST.get('description', '')
        a_start_price = request.POST.get('start_price', '')
        tmp_end_time = request.POST.get('endtime', '')

        a_end_time=datetime.strptime(tmp_end_time,'%Y-%m-%d %H:%M') #'%Y-%m-%d %H:%M'

        auction = Auction(seller=a_seller,title =a_title, description = a_description, start_price=a_start_price, endtime=a_end_time)
        auction.save()
        messages.add_message(request, messages.INFO, "New auction has been saved")
        return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponseRedirect(reverse("home"))
def browseauctions(request):
    auctions=Auction.objects.all().order_by('title')
    #auctions=Auction.objects.order_by('-endtime')
    return render(request, "auctions.html", {'auctions':auctions})

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
    show_results=False
    query=request.GET.get('q','')
    if query:
        query=query.strip()
        form = Searchingform({'query':query})
        auctions=Auction.objects.filter(title__icontains=query)[:10]
    else:
        auctions=[]

    return render(request,"searchauction.html",{'auctions': auctions,'query':query})

