import base64

from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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

@method_decorator(csrf_exempt, name="dispatch")
class BlogDetailApi(View):
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.pk = kwargs["pk"]
        # Look up the user and throw a 404 if it doesn't exist
        #self.user = get_object_or_404(User, username=username)

        if not request.method in ["GET","PUT","DELETE"]:
            return HttpResponseNotAllowed(["GET","PUT","DELETE"])
        # Check and store HTTP basic authentication, even for methods that
        # don't require authorization.

        self.authenticate_user()
        if self.authenticated_user is None:
            return HttpResponseForbidden()

        # Call the request method handler
        return super(BlogDetailApi, self).dispatch(request, *args, **kwargs)

    def authenticate_user(self):
        # Pull the auth info out of the Authorization: header
        auth_info = self.request.META.get("HTTP_AUTHORIZATION", None)

        print (auth_info)
        if auth_info and auth_info.startswith("Basic "):
            basic_info = auth_info.split(" ", 1)[1]
            decode_info = base64.b64decode(basic_info)
            print (decode_info)
            u, p = str(decode_info, 'utf-8').split(":")
            print (u, p)

            self.user = u
            # Authenticate against the User database. This will set
            # authenticated_user to None if authentication fails.
            self.authenticated_user = authenticate(username=u, password=p)
            print ("self.authenticated_user,", self.authenticated_user)
        else:
            self.authenticated_user = None

    def forbidden(self):
        response = HttpResponseForbidden()
        response["WWW-Authenticate"] = 'Basic realm="BlogPost"'
        return response

    def delete(self, *args, **kwargs):
        # Look up the bookmark...
        auction = get_object_or_404(Auction, id=self.pk)
        # ... and delete it.
        auction.delete()
        # Return a 204 ("no content")
        response = HttpResponse()
        response.status_code = 204
        return response

    def get(self, *args, **kwargs):
        return HttpResponse("This is Get Method")

    def put(self, *args, **kwargs):
        print(self.request.body)
        return HttpResponse("This is PUT Method")