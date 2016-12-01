"""restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from quickstart import views
from django.conf.urls.static import static
from django.conf import settings







urlpatterns = [
    url(r'^quickstart/(?P<sortmethod>(top|new)?)/?$', views.SnippetList.as_view()),
    url(r'^quickstart/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'^comments/(?P<id>[0-9]+)/$', views.CommentList.as_view()),
    url(r'^comment/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view()),
    url(r'^quickstart/(?P<pk>[0-9]+)/(?P<value>-?(up|down))/$', views.IncrementVotes, name='InvrementVotes'),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^register/$', views.Register.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from rest_framework.authtoken import views
urlpatterns += [url(r'^get-token/', views.obtain_auth_token)]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))]


from django.contrib.staticfiles import views

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)
