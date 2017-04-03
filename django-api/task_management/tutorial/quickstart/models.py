from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from static import TASK_STATUS, USER_TYPE

# Create your models here.


class user_db(models.Model):
        username = models.EmailField(primary_key=True)
        usertype = models.PositiveSmallIntegerField(choices=USER_TYPE)
        password = models.TextField()


class task_table(models.Model):
    assignee = models.ManyToManyField(user_db, related_name="student")
    admin = models.ForeignKey(user_db)
    title = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(choices=TASK_STATUS)

