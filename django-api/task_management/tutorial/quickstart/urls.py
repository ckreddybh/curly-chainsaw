
from django.conf.urls import url, include
from tutorial.quickstart.views import *


urlpatterns = [
    url(r'taskcreate/', TaskView.as_view(), name='taskcreate'),
    url(r'user/', UserDB.as_view(), name='user'),
    url(r'statusupdate/', TaskUpdateStatus.as_view(), name='updatestatus'),
    url(r'assigneeupdate/', TaskUpdateAddAssignees.as_view(), name='updateassignee'),
    url(r'assigneedelete/', TaskUpdateDeleteAssignees.as_view(), name='updateassignee'),
    url(r'taskdelete/', TaskDelete.as_view(), name='taskdelete'),
]