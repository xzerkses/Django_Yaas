from rest_framework import serializers

from YAAS_App.models import Pid, Auction


class PidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pid
        fields = ('auction_id','seller' 'pid_value','pid_datetime',)


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields =('auction_status','title','description','start_price','latest_pid','endtime',)
