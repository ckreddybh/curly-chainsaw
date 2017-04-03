# from django.contrib.auth.models import User, Group
# from rest_framework import viewsets
# from tutorial.quickstart.serializers import UserSerializer, GroupSerializer, taskSerializer
# from rest_framework import IsAdminUser, SAFE_METHODS
from tutorial.quickstart.models import task_table, user_db
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from django.contrib.auth import authenticate, login, logout
import hashlib
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import QueryDict
from django.forms.models import model_to_dict
from static import TASK_STATUS, USER_TYPE, ADMIN_TASK_STATUS


def auth_dec_get(func):
    def _auth_valid(request):
        method = request.method
        if method == 'POST':
            data = request.POST
        elif method == 'GET':
            data = request.GET
        else:
            data = QueryDict(request.body)
            # import pdb;pdb.set_trace()
    # http://stackoverflow.com/questions/4994789/django-where-are-the-params-stored-on-a-put-delete-request
    # request.body is not in correct format as expected need to check
        username = data.get('logid', None)
        password = hashlib.sha512(data.get('logpass', '')).hexdigest()
        try:
            # import pdb;pdb.set_trace()
            user = user_db.objects.get(username=username, password=password)
        except user_db.DoesNotExist as e:
            return HttpResponse(json.dumps(
                {'error': 'Invalid credentials, Please check logid and logpass',
                    'logid': username,
                    'logpass': data.get('logpass', None)}),
                content_type='application/json')
        if not user:
            return HttpResponse('Invalid credentials')
        return func(request)
    return _auth_valid


def auth_dec_admin(func):
    def _auth_valid(request):
        method = request.method
        if method == 'POST':
            data = request.POST
        elif method == 'GET':
            data = request.GET
        else:
            data = QueryDict(request.body)
        # http://stackoverflow.com/questions/4994789/django-where-are-the-params-stored-on-a-put-delete-request
        username = data.get('logid', None)
        password = hashlib.sha512(data.get('logpass', '')).hexdigest()
        try:
            user = user_db.objects.get(username=username, password=password, 
                                       usertype=1)
        except user_db.DoesNotExist as e:
            try:
                user = user_db.objects.get(username=username, password=password)
            except user_db.DoesNotExist:
                return HttpResponse(json.dumps(
                {'error': 'Invalid credentials, Please check logid and logpass',
                    'logid': username,
                    'logpass': data.get('logpass', None)}),
                content_type='application/json')
            return HttpResponse(json.dumps(
                {'error': 'Not authorized user, User should be `admin`',
                    'logid': username,
                    'logpass': data.get('logpass', None),
                    'user_type': dict(USER_TYPE).get(user.usertype)}),
                content_type='application/json')
        if not user:
            return HttpResponse('Invalid credentials')
        return func(request)
    return _auth_valid


class UserDB(View):

    @method_decorator(csrf_exempt)
    @method_decorator(auth_dec_get)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDB, self).dispatch(request, *args, **kwargs)

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
    def isvalid_field(params, error):
        # error = []
        if not params.get('username'):
            print 'username'
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
            return None
        if not UserDB.isvalid_type(params.get('usertype'), error):
            print 'usertype'
            return None
        print 'success...valid'
        return True

    @method_decorator(auth_dec_admin)
    def post(self, request):
        params = request.POST
        error = []
        # if not UserDB.isvalid_field(params, error):
        #     params_required = {'username': '<user_id>',
        #                        'usertype': '1 for admin 2 for student',
        #                        'password': '<pass_for_user>'}
        #     return HttpResponse(json.dumps(
        #                             {'error': 'Invalid params',
        #                              'required_params': params_required}),
        #                         content_type='application/json')
        data = {
            'username': params.get('username'),
            'usertype': params.get('usertype'),
            'password': hashlib.sha512(params.get('password')).hexdigest()
        }
        data_dump = None
        if UserDB.isvalid_field(data, error):
            obj = user_db.objects.create(**data)
            data_dump = model_to_dict(obj)

        return HttpResponse(json.dumps([error, data_dump]), content_type='application/json')
    
    def get(self, request):
        objs = user_db.objects.all()
        data = []
        for obj in objs:
            data.append({'username': obj.username,
                         'usertype': obj.usertype})
        return HttpResponse(json.dumps(data), content_type='application/json')


class static_methods():

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
            return TaskView.isValid_status(status, error)
        if assignee_list:
            return static_methods.isValid_assignee(assignee_list, error)

    @staticmethod
    def getStatus(status_id):
        return dict(TASK_STATUS).get(
                        status_id, dict(ADMIN_TASK_STATUS).get(
                            status_id, None))

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
        params = static_methods.get_params(request)
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
        params = static_methods.get_params(request)
        logid = request.POST.get('logid', None)
        try:
            assignee_list = static_methods.process_user_list(
                task_obj.assignee.all())
            if logid in assignee_list:
                return True
            return False
        except user_db.DoesNotExist as e:
            return False


class TaskDelete(View, static_methods):
    @method_decorator(csrf_exempt)
    @method_decorator(auth_dec_get)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskDelete, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth_dec_admin)
    def post(self, request):
        params = request.POST
        task_id = params.get('task_id', None)
        try:
            # import pdb;pdb.set_trace()
            task_obj = task_table.objects.get(id=task_id).delete()
        except task_table.DoesNotExist as e:
            return HttpResponse(json.dumps(
                    {'error': 'No task found with the given id',
                        'task_id_given': task_id}),
                    content_type='application/json')
        return HttpResponse(json.dumps(
                                {'error': '',
                                 'task_id': task_id,
                                 'status': 'Deleted successfully'}),
                            content_type='application/json')


class TaskUpdateStatus(View, static_methods):
    
    @method_decorator(csrf_exempt)
    @method_decorator(auth_dec_get)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskUpdateStatus, self).dispatch(request, *args, **kwargs)

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
    def is_diff_1(old_status, new_status):
        if not dict(TASK_STATUS).get(new_status, None):
            return False
        if abs(old_status - new_status) <= 1:
            return True
        return False

    def post(self, request):

        params_required = {'logid': '<user_id>',
                           'logpass': '<user_pass>',
                           'task_id': '<task_to_update>'}
        perams_optional = {'status': 'new_status \
        if not specified assumes current status as new status'}
        params = request.POST
        task_id = params.get('task_id', None)
        try:
            task_obj = task_table.objects.get(id=task_id)
        except task_table.DoesNotExist as e:
            return HttpResponse(json.dumps(
                    {'error': 'No task found with the given id',
                        'task_id_given': task_id,
                        'params': {'optional': perams_optional,
                                   'required': params_required}}),
                    content_type='application/json')
        status = int(params.get('status', None))
        old_status = None
        if not status:
            status = task_obj.status
            old_status = status
        else:
            old_status = task_obj.status
        # import pdb;pdb.set_trace()
        if TaskView.isAdmin(request):
            if dict(ADMIN_TASK_STATUS).get(status, None) and old_status == 3:
                task_obj.status = status
                task_obj.save()
                data = model_to_dict(task_obj)
                return HttpResponse(json.dumps(
                        {'': 'Status changed successfully',
                         'old_status': TaskUpdateStatus.getStatus(old_status),
                         'new_status': TaskUpdateStatus.getStatus(status),
                         'fields': data}),
                                        content_type='application/json')
            elif dict(ADMIN_TASK_STATUS).get(status, None):
                return HttpResponse(json.dumps(
                        {'error': 'Invalid new status',
                         'old_status': TaskUpdateStatus.getStatus(old_status),
                         'new_status': TaskUpdateStatus.getStatus(status),
                         'valid_move': 'done -> approve or done -> disapprove',
                         'params': {'optional': perams_optional,
                                    'required': params_required}}),
                                    content_type='application/json')
        if TaskUpdateStatus.isAssignee(request, task_obj):
            
            # import pdb;pdb.set_trace()
            if dict(ADMIN_TASK_STATUS).get(old_status, None) and status != old_status:
                return HttpResponse(json.dumps(
                        {'error': 'Invalid new status, you should be admin',
                         'old_status': TaskUpdateStatus.getStatus(old_status),
                         'new_status': TaskUpdateStatus.getStatus(status),
                         'valid_move': 'student can do only todo <-> doing <-> done'}),
                                    content_type='application/json')
            if TaskUpdateStatus.is_diff_1(old_status, status):
                task_obj.status = status
                task_obj.save()
                data = model_to_dict(task_obj)
                return HttpResponse(json.dumps(
                        {'': 'Status changed successfully',
                         'old_status': TaskUpdateStatus.getStatus(old_status),
                         'new_status': TaskUpdateStatus.getStatus(status),
                         'fields': data}),
                                        content_type='application/json')
            else:
                return HttpResponse(json.dumps(
                        {'error': 'Invalid new status',
                         'old_status': TaskUpdateStatus.getStatus(old_status),
                         'new_status': TaskUpdateStatus.getStatus(status),
                         'valid_move': 'todo <-> doing <-> done'}),
                                    content_type='application/json')
        if TaskView.isAdmin(request):
            return HttpResponse(json.dumps(
                        {'error': 'Adim can approve or disapprove if he is not assignee',
                         'current_user': params.get('logid', None),
                         'task_id': task_id}),
                                    content_type='application/json')
        return HttpResponse(json.dumps(
                        {'error': 'Invalid user, Current user is not assignee',
                         'current_user': params.get('logid', None),
                         'task_id': task_id}),
                                    content_type='application/json')


class TaskUpdateAddAssignees(View, static_methods):
    @method_decorator(csrf_exempt)
    @method_decorator(auth_dec_get)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskUpdateAddAssignees, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth_dec_admin)
    def post(self, request):
        params_required = {'title'}
        params_optional = {'assignee'}
        params = request.POST
        error = {}
        error_list = []
        if params.get('assignee', None):
            assignee_list = params.get('assignee').split(',')
        else:
            assignee_list = None

        data = {'task_id': params.get('task_id', None),
                'assignee': assignee_list}
        if not TaskUpdateAddAssignees.isValid_assignee(assignee_list,
                                                       error_list):
            print error
            # import pdb;pdb.set_trace()
            error['error'] = error_list
            error['fields'] = data
            return HttpResponse(json.dumps(error),
                                content_type='application/json')
        try:
            obj = task_table.objects.get(id=data.get('task_id'))
        except:
            return HttpResponse(json.dumps(
                    {'error': 'No task found with the given id',
                        'task_id_given': task_id}),
                    content_type='application/json') 
        # import pdb;pdb.set_trace()
        # obj.save()
        if assignee_list:
            assignee_list = params.get('assignee').split(',')
            # for assignee in assignee_list:
            obj.assignee.add(*assignee_list)
            obj.save()
        return HttpResponse(json.dumps(model_to_dict(obj)),
                            content_type='application/json')


class TaskUpdateDeleteAssignees(View, static_methods):
    @method_decorator(csrf_exempt)
    @method_decorator(auth_dec_get)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskUpdateDeleteAssignees, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth_dec_admin)
    def post(self, request):
        params_required = {'title'}
        params_optional = {'assignee'}
        params = request.POST
        error = {}
        error_list = []
        if params.get('assignee', None):
            assignee_list = params.get('assignee').split(',')
        else:
            assignee_list = None

        data = {'task_id': params.get('task_id', None),
                'assignee': assignee_list}
        if not TaskUpdateDeleteAssignees.isValid_assignee(assignee_list,
                                                          error_list):
            print error
            # import pdb;pdb.set_trace()
            error['error'] = error_list
            error['fields'] = data
            return HttpResponse(json.dumps(error),
                                content_type='application/json')
        try:
            obj = task_table.objects.get(id=data.get('task_id'))
        except:
            return HttpResponse(json.dumps(
                    {'error': 'No task found with the given id',
                        'task_id_given': task_id}),
                    content_type='application/json') 
        # import pdb;pdb.set_trace()
        # obj.save()
        if assignee_list:
            assignee_list = params.get('assignee').split(',')
            # for assignee in assignee_list:
            error = {'log': 'Users deleted',
                     'deleted_list': assignee_list}
            obj.assignee.remove(*assignee_list)
            obj.save()
        return HttpResponse(json.dumps([error, model_to_dict(obj)]),
                            content_type='application/json')


class TaskView(View, static_methods):

    @method_decorator(csrf_exempt)
    @method_decorator(auth_dec_get)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskView, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth_dec_admin)
    def post(self, request):
        params_required = {'title'}
        params_optional = {'assignee'}
        params = request.POST
        error = {}
        error_list = []
        if params.get('assignee', None):
            assignee_list = params.get('assignee').split(',')
        else:
            assignee_list = None

        data = {'title': params.get('title', None),
                'status': 1,
                'admin_id': params.get('logid', None)}
        if not TaskView.isvalid_field(data, assignee_list, error_list):
            print error
            # import pdb;pdb.set_trace()
            error['error'] = error_list
            error['fields'] = data
            return HttpResponse(json.dumps(error), content_type='application/json')
        obj = task_table.objects.create(**data)
        # import pdb;pdb.set_trace()
        obj.save()
        if assignee_list:
            assignee_list = params.get('assignee').split(',')
            for assignee in assignee_list:
                obj.assignee.add(assignee)
        return HttpResponse(json.dumps(model_to_dict(obj)),
                            content_type='application/json')

    def get(self, request):
        params = request.GET
        data = []
        if TaskView.isAdmin(request):
            task_objs = task_table.objects.all()
            for task_obj in task_objs:
                task_obj.save()
                print task_obj.assignee.all()
                status = TaskView.getStatus(task_obj.status)
                data.append({'task_id': task_obj.id,
                             'title': task_obj.title,
                             'status': status,
                             'admin_id': task_obj.admin_id,
                             'assignee_id': TaskView.process_user_list(
                                task_obj.assignee.all())})
        else:
            # import pdb; pdb.set_trace()
            task_objs = task_table.objects.all()
            for task_obj in task_objs:
                task_obj.save()
                print task_obj.assignee.all()
                assignee_list = TaskView.process_user_list(
                                    task_obj.assignee.all())
                if params.get('logid') in assignee_list:
                    status = TaskView.getStatus(task_obj.status)
                    data.append({'task_id': task_obj.id,
                                 'title': task_obj.title,
                                 'status': status,
                                 'admin_id': task_obj.admin_id,
                                 'assignee_id': assignee_list})
        print data
        # import pdb; pdb.set_trace()
        return HttpResponse(json.dumps(data), content_type='application/json')
