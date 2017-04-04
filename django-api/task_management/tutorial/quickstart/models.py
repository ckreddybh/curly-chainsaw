from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from static import TASK_STATUS, USER_TYPE, ADMIN_TASK_STATUS
from django.http import QueryDict

# Create your models here.


class user_db(models.Model):
    username = models.EmailField(primary_key=True)
    usertype = models.PositiveSmallIntegerField(choices=USER_TYPE)
    password = models.TextField()

    @staticmethod
    def isvalid_type(user_type, error):
        user_type = int(user_type)
        valid_status = dict(USER_TYPE).get(user_type, None)
        # import pdb;pdb.set_trace()
        if valid_status:
            return True
        error.append({'error': 'Invalid user type',
                      'usertype_given': user_type,
                      'valid_type': dict(USER_TYPE)})
        return False

    @staticmethod
    def isvalid_user_params(params, error):
        # error = []
        required_params = {
            'username': '<new_username>',
            'password': '<password for user>',
            'usertype': '1,2 (1=> admin 2=> student)'
        }
        if not params.get('username'):
            print 'username'
            error.append({'error': 'username missing',
                          'required_params': required_params})
            return False
        else:
            try:
                user_db.objects.get(username=params.get('username'))
                print 'user already found'
                error.append({'error': 'Invalid!!, User already exist'})
                return None
            except user_db.DoesNotExist as e:
                print "user not found creating one"
        if not params.get('password'):
            print 'password'
            error.append({'error': 'Password field missing',
                          'required_params': required_params})
            return None
        if not user_db.isvalid_type(params.get('usertype'), error):
            print 'usertype'
            error.append({'error': 'Invalid! usertype, User already exist',
                          'required_params': required_params})
            return None
        print 'success...valid'
        return True


class task_table(models.Model):
    assignee = models.ManyToManyField(user_db, related_name="student")
    admin = models.ForeignKey(user_db)
    title = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(choices=TASK_STATUS)

    @staticmethod
    def getStatus(status_id):
        return dict(TASK_STATUS).get(
                        status_id, dict(ADMIN_TASK_STATUS).get(
                            status_id, None))

    @staticmethod
    def isValid_assignee(assignee, error_list):
        if not isinstance(assignee, list):
            assignee_list = [assignee]
        else:
            assignee_list = assignee
        for assignee in assignee_list:
            try:
                user = user_db.objects.get(username=assignee)
            except user_db.DoesNotExist as e:
                error_list.append({'error': 'No user exist, Assignee not found please check',
                                  'assignee': assignee})
                return False
        return True

    @staticmethod
    def isvalid_field(data, assignee_list, error):
        title = data.get('title')
        status = data.get('status')
        assignee_list = assignee_list
        if not title:
            return False
        else:
            if len(title) > 100:
                error.append({'error': 'title is out of length, not more than 100 chars',
                              'title': title})
                return False
                        
        if not status:
            return False
        else:
            return task_table.isValid_status(status, error)
        if assignee_list:
            return task_table.isValid_assignee(assignee_list, error)

    @staticmethod
    def is_diff_1(old_status, new_status):
        if not dict(TASK_STATUS).get(new_status, None):
            return False
        if abs(old_status - new_status) <= 1:
            return True
        return False

    @staticmethod
    def isValid_status(status, error):

        valid_status = dict(TASK_STATUS).get(status, None)
        if valid_status:
            return True
        error.append({'error': 'Invalid status',
                      'status_given': status,
                      'valid_status': dict(TASK_STATUS)})
        return False

    @staticmethod
    def get_params(request):
        method = request.method
        data = None
        if method == 'POST':
            data = request.POST
        elif method == 'GET':
            data = request.GET
        else:
            data = QueryDict(request.body)
        return data

    @staticmethod
    def isAdmin(request):
        params = task_table.get_params(request)
        try:
            user_db.objects.get(username=params.get('logid'), usertype=1)
            return True
        except user_db.DoesNotExist as e:
            return False

    @staticmethod
    def process_user_list(user_db):
        return [x.username for x in user_db]

    @staticmethod
    def isAssignee(request, task_obj):
        params = task_table.get_params(request)
        logid = request.POST.get('logid', None)
        try:
            assignee_list = task_table.process_user_list(
                task_obj.assignee.all())
            if logid in assignee_list:
                return True
            return False
        except user_db.DoesNotExist as e:
            return False
