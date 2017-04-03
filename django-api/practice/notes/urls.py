from django.conf.urls import url, include
from notes.views import *
from tastypie.api import Api
from models import NoteResource


v1_api = Api(api_name='v1')
v1_api.register(NoteResource())


urlpatterns = [
    url(r'^index/', index, name='index'),
    url(r'^dashboard/', dashboard, name='dashboard'),
    url(r'^logout/', dologout, name='logout '),
    url(r'^api/', include(v1_api.urls)),

]