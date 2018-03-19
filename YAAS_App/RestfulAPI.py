import base64
from datetime import timedelta, datetime

from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from YAAS_App.forms import AddPid
from YAAS_App.views import check_endingtime
from .models import Auction, Pid
from .serializers import PidSerializer, AuctionSerializer
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed, request




class AuctionList(APIView):
    def get(self, request):
        try:
            auctions = Auction.objects.all()
        except Auction.DoesNotExist:
            return HttpResponse(status=404)
        serialized_data = AuctionSerializer(auctions, many=True)
        # return HttpResponse(serialized_data, content_type="application/json")
        return Response(serialized_data.data)


class AuctionSearch(APIView):

        def get(self, request,pk):
            try:
                auction = Auction.objects.get(pk=pk)
            except Auction.DoesNotExist:
                return HttpResponse(status=404)
            serialized_data = AuctionSerializer(auction)
            #return HttpResponse(serialized_data, content_type="application/json")
            return Response(serialized_data.data)

         # def put(self,request,pk):
         #     print("put")


class TokenAuthAddPid(APIView):
    auth_classes=(TokenAuthentication,)
    permission_classes(IsAuthenticated,)
    # if request.method=='GET':
    #      serializer = PidSerializer()
    # return Response(serializer.data)

    def put(self, request,pk):

        try:
            auction=Auction.objects.get(pk=pk)
        except auction.DoesNotExist:
            return HttpResponse(status=404)
        data=request.data


        new_pidvalue = data.get('pid_value')
        print(auction)
        if Decimal(new_pidvalue) < Decimal(0.01) + auction.latest_pid:
            #messages.add_message(request, messages.ERROR, "Pid value must be at least 0.01€ higher than previous pid.")
            return HttpResponse(status=404) #incorrect value

        if (check_endingtime(auction.endtime - timedelta(minutes=5))):
            auction.endtime = auction.endtime + timedelta(minutes=5)
            auction.save()

        if check_endingtime(auction.endtime):
            #return HttpResponse(status=408)
            auction.auction_status = 'C'
            auction.save()
            return Response(status=408)

        pid = Pid(pidder=request.user, auction_id=auction, pid_value=new_pidvalue, pid_datetime=datetime.now())
        pid.save()
        return Response(status=200)




