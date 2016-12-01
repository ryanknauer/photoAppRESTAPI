from __future__ import unicode_literals

from django.db import models

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token

# Create your models here.from django.conf import settings
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver




LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
    Latitude = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    Longitude = models.DecimalField(max_digits=8, decimal_places=3, null=True)
    photo = models.FileField(upload_to='photos/', null=True)
    rank = models.IntegerField(default=1)
    votes = models.IntegerField(default=0)
    upVotes = models.ManyToManyField(User, related_name='upVotedOn')
    downVotes = models.ManyToManyField(User, related_name='downVotedOn')
    owner = models.ForeignKey('auth.User', related_name='snippets')
    mediaType = models.CharField(max_length=10, null=False)
    class Meta:
        ordering = ('-votes', '-id')


@receiver(pre_delete, sender=Snippet)
def snippet_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.photo:
        instance.photo.delete(False)



class Comment(models.Model):
    comment = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='comments')
    snippet = models.ForeignKey('Snippet', related_name='comments')
    class Meta:
        ordering = ('snippet',)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




