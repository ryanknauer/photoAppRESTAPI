from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from quickstart.models import Snippet, Comment
from quickstart.serializers import SnippetSerializer, CommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework import permissions
from rest_framework import generics
from django.db.models import F
from quickstart.serializers import UserSerializer
from quickstart.serializers import RegistrationSerializer
from quickstart.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods


class SnippetList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    
    """

    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        sortMethod = self.kwargs['sortmethod']
        print(sortMethod)
        if sortMethod == 'new':
            return Snippet.objects.all().order_by('-id')
        else:
            return Snippet.objects.all()





class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    
    """
    Retrieve, update or delete a snippet instance.
    """

    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CommentList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        id = self.kwargs['id']
        obj = Snippet.objects.get(id=id)
        serializer.save(owner=self.request.user, snippet=obj)

    def get_queryset(self):
        id = self.kwargs['id']
        return Comment.objects.filter(snippet=id)
                         


        

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    
    """
    Retrieve, update or delete a snippet instance.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Register(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view()
def IncrementVotes(request, pk, value):
    obj = Snippet.objects.get(id=pk)
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        if value == "up":
            obj.upVotes.add(user)
            obj.downVotes.remove(user)
        elif value == "down":
            obj.downVotes.add(user)
            obj.upVotes.remove(user)
        elif value == "-down":
            obj.downVotes.remove(user)
        elif value == "-up":
            obj.upVotes.remove(user)
    
        obj.votes = obj.upVotes.count() - obj.downVotes.count()
        obj.save()
        return(HttpResponse("done"))
    else:
        return(HttpResponse("notAuth"))


'''    if value == "up":
        Snippet.objects.filter(id=pk).update(votes=F('votes') + 1)
    elif value == "down" :
        Snippet.objects.filter(id=pk).update(votes=F('votes') - 1)
    return(HttpResponse("done"))'''





    


