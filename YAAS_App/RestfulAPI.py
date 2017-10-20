import base64
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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




# class TokenAuthAddPid(APIView):
#     #auth_classes=(TokenAuthentication,)
#     #permission_classes(IsAuthenticated,)
#     # if request.method=='GET':
#     #     serializer = PidSerializer()
#     #     return Response(serializer.data)
#
#     def put(self, request,offset):
#         print("1st täällä")
#         data=request.DATA
#
#         serialized_data=PidSerializer(data=data)
#         if serialized_data.is_valid():
#             serialized_data.save(serialized_data.data,status=201)
#             print("onnistui täällä")
#
#         else:
#             return Response(serialized_data.errors, status=404)

