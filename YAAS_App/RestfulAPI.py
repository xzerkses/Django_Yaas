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

from django.core import serializers
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

#from YAAS_App.models import Auction

# def auctions_list(request):
#     auctions = Auction.objects.all()
#     auctions_json = serializers.serialize("json", auctions)
#     return HttpResponse(auctions_json, content_type="application/json")
#
# def search_auction(request, offset):
#         auction=Auction.objects.filter(id=offset)
#
#         if(auction.exists()):
#             auction_json=serializers.serialize("json",auction)
#             return HttpResponse(auction_json, content_type="application/json")
#         else:
#             print("tööt")
#             response=HttpResponse()
#             response.status_code = 404
#             return response

class AuctionList(APIView):
    def get(self, request):
        try:
            auctions = Auction.objects.all()
        except Auction.DoesNotExist:
            return HttpResponse(status=404)
        serialized_data = AuctionSerializer(auctions, many=True)
        # return HttpResponse(serialized_data, content_type="application/json")
        return Response(serialized_data.data)
    # def get(self, request):
    #
    #     auctions=Auction.objects.all()
    #     serialized_data=AuctionSerializer(auctions, many=True)
    #     #return HttpResponse(serialized_data, content_type="application/json")
    #     return Response(serialized_data.data, content_type="application/json")


class AuctionSearch(APIView):

    def get(self, request,pk):
        try:
            auction = Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            return HttpResponse(status=404)
        serialized_data = AuctionSerializer(auction)
        #return HttpResponse(serialized_data, content_type="application/json")
        return Response(serialized_data.data)



# def search_auction(request,pk):
#     auction=Auction.objects.get(pk=pk)
#     serialized_data=AuctionSerializer(auction)
#     print(serialized_data)
#     return Response(serialized_data.data)
#
#
class TokenAuthAddPid(APIView):
    auth_classes=(TokenAuthentication,)
    permission_classes(IsAuthenticated,)
    # if request.method=='GET':
    #     serializer = PidSerializer()
    #     return Response(serializer.data)

    def put(self, request):
        print("1st täällä")
        data=request.DATA

        serialized_data=PidSerializer(data=data)
        if serialized_data.is_valid():
            serialized_data.save(serialized_data.data,status=201)
            print("onnistui täällä")

        else:
            return Response(serialized_data.errors, status=404)
#
# @api_view(['GET', 'POST'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def auction_detail(request, pk):
#
#     try:
#         blog = Auction.objects.get(pk=pk)
#     except Auction.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = PidSerializer(blog)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         data = request.DATA
#         print(request.DATA)
#         serializer = PidSerializer(blog, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)

# @api_view(['GET'])
# @renderer_classes([JSONRenderer,])
# def blog_list(request):
#     if request.method == 'GET':
#         blogs = BlogPost.objects.all()
#         serializer = BlogPostSerializer(blogs, many=True)
#         return Response(serializer.data)

