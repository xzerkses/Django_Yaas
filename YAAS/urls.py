"""YAAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from django.contrib.auth import views

from YAAS_App.RestfulAPI import *
from YAAS_App.views import *


urlpatterns = [
    url(r'^$',browseauctions, name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^createuser/$',register_user),
    url(r'^createauction/$', AddAuction.as_view(), name="add_auction"),
    url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
    url(r'^saveauction/$', saveauction),
    url(r'^savechanges/(\d+)/$', savechanges),
    url(r'^editauction/(\d+)/$', editauction),
    url(r'^searchauction/$', search),
    url(r'^readjson/$', readJson),
    url(r'^addpid/(\d+)$', addpid),
    url(r'^savepid/(\d+)$', savepid),
    url(r'^banview/(\d+)$', banview),
    url(r'^banauction/(\d+)$', ban),
    url(r'^auctions/$', auctions_list),
    url(r'^auctions/(\d+)$', search_auction),
    url(r'^get_highest_pid/(\d+)$', getWinner),
    url(r'^api/auctions/(?P<pk>\d+)/$', BlogDetailApi.as_view()),

    #url(r'^sendview/$', sendview, name="sendmsg"),
]