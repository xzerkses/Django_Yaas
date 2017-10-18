
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core import serializers

from YAAS_App.models import Auction

def auctions_list(request):
    auctions = Auction.objects.all()
    auctions_json = serializers.serialize("json", auctions)
    return HttpResponse(auctions_json, content_type="application/json")

def search_auction(request, offset):
        auction=Auction.objects.filter(id=offset)

        if(auction.exists()):
            auction_json=serializers.serialize("json",auction)
            return HttpResponse(auction_json, content_type="application/json")
        else:
            print("tööt")
            response=HttpResponse()
            response.status_code = 404
            return response
