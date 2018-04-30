from rest_framework import serializers

from YAAS_App.models import Bid, Auction


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('Bid_value',) #'auction_id','Bidder',


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields =('auction_status','title','description','start_price','latest_Bid','endtime',)
