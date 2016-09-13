from rest_framework import serializers
from quickstart.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES, Comment
from django.contrib.auth.models import User




class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    upVotes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')
    downVotes = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    
    class Meta:
        model = Snippet
        fields = ('id', 'Latitude', 'Longitude', 'photo', 'rank', 'votes', 'owner', 'upVotes', 'downVotes', 'comments')
        read_only_fields = ('id', 'rank', 'votes','owner', 'upVotes', 'downVotes', 'comments')


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    snippet = serializers.ReadOnlyField(source='snippet.id')
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'owner', 'snippet')
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    upVotedOn = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    downVotedOn = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())
    
    class Meta:
        model = User
        fields = ('id', 'username', 'snippets', 'upVotedOn', 'downVotedOn',  'comments')
        read_only_fields = ('snippets', 'upVotedOn', 'downVotedOn')



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
