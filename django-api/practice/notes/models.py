from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms


from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class Note(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    creaeTime = models.DateTimeField()


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        # exclude = ['owner']


class NoteResource(ModelResource):
    class Meta:
        queryset = Note.objects.all()
        resource_name = 'note'
        authorization = Authorization()
