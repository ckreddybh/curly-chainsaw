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
from tutorial.quickstart.static import TASK_STATUS, USER_TYPE, ADMIN_TASK_STATUS


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

    @method_decorator(auth_dec_admin)
    def post(self, request):
        params = request.POST
        error = []
        data = {
            'username': params.get('username'),
            'usertype': params.get('usertype', 2),
            'password': params.get('password')
        }
        data_dump = None
        if user_db.isvalid_user_params(data, error):
            data['password'] = hashlib.sha512(data['password']).hexdigest()
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


class TaskDelete(View):
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


class TaskUpdateStatus(View):

    @method_decorator(csrf_exempt)
    @method_decorator(auth_dec_get)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskUpdateStatus, self).dispatch(request, *args, **kwargs)

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
        if task_table.isAdmin(request):
            if dict(ADMIN_TASK_STATUS).get(status, None) and old_status == 3:
                task_obj.status = status
                task_obj.save()
                data = model_to_dict(task_obj)
                return HttpResponse(json.dumps(
                        {'': 'Status changed successfully',
                         'old_status': task_table.getStatus(old_status),
                         'new_status': task_table.getStatus(status),
                         'fields': data}),
                                        content_type='application/json')
            elif dict(ADMIN_TASK_STATUS).get(status, None):
                return HttpResponse(json.dumps(
                        {'error': 'Invalid new status',
                         'old_status': task_table.getStatus(old_status),
                         'new_status': task_table.getStatus(status),
                         'valid_move': 'done -> approve or done -> disapprove',
                         'params': {'optional': perams_optional,
                                    'required': params_required}}),
                                    content_type='application/json')
        if task_table.isAssignee(request, task_obj):
            # import pdb;pdb.set_trace()
            if dict(ADMIN_TASK_STATUS).get(old_status, None) and status != old_status:
                return HttpResponse(json.dumps(
                        {'error': 'Invalid new status, you should be admin',
                         'old_status': task_table.getStatus(old_status),
                         'new_status': task_table.getStatus(status),
                         'valid_move': 'student can do only todo <-> doing <-> done'}),
                                    content_type='application/json')
            if task_table.is_diff_1(old_status, status):
                task_obj.status = status
                task_obj.save()
                data = model_to_dict(task_obj)
                return HttpResponse(json.dumps(
                        {'': 'Status changed successfully',
                         'old_status': task_table.getStatus(old_status),
                         'new_status': task_table.getStatus(status),
                         'fields': data}),
                                        content_type='application/json')
            else:
                return HttpResponse(json.dumps(
                        {'error': 'Invalid new status',
                         'old_status': task_table.getStatus(old_status),
                         'new_status': task_table.getStatus(status),
                         'valid_move': 'todo <-> doing <-> done'}),
                                    content_type='application/json')
        if task_table.isAdmin(request):
            return HttpResponse(json.dumps(
                        {'error': 'Admin can approve or disapprove if he is not assignee',
                         'log': 'looks like sutend dint finish task wait for task to be marked as done (3)',
                         'current_user': params.get('logid', None),
                         'task_id': task_id}),
                                    content_type='application/json')
        return HttpResponse(json.dumps(
                        {'error': 'Invalid user, Current user is not assignee',
                         'current_user': params.get('logid', None),
                         'task_id': task_id}),
                                    content_type='application/json')


class TaskUpdateAddAssignees(View):
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
        if not task_table.isValid_assignee(assignee_list,
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
                        'task_id_given': data.get('task_id')}),
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


class TaskUpdateDeleteAssignees(View):
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
        if not task_table.isValid_assignee(assignee_list,
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
                     'task_id_given': data.get('task_id')}),
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


class TaskView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(auth_dec_get)
    def dispatch(self, request, *args, **kwargs):
        return super(TaskView, self).dispatch(request, *args, **kwargs)

    @method_decorator(auth_dec_admin)
    def post(self, request):
        params_required = {
            'title': '<title of the task>',
        }
        params_optional = {'assignee': 'username <if required multiple comma separated assignees>'}
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
        if not task_table.isvalid_field(data, assignee_list, error_list):
            print error
            # import pdb;pdb.set_trace()
            error['error'] = error_list
            error['fields'] = data
            return HttpResponse(json.dumps([error, {'params_required': params_required, 'params_optional': params_optional}]), content_type='application/json')
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
        if task_table.isAdmin(request):
            task_objs = task_table.objects.all()
            for task_obj in task_objs:
                task_obj.save()
                print task_obj.assignee.all()
                status = task_table.getStatus(task_obj.status)
                data.append({'task_id': task_obj.id,
                             'title': task_obj.title,
                             'status': status,
                             'admin_id': task_obj.admin_id,
                             'assignee_id': task_table.process_user_list(
                                task_obj.assignee.all())})
        else:
            # import pdb; pdb.set_trace()
            task_objs = task_table.objects.all()
            for task_obj in task_objs:
                task_obj.save()
                print task_obj.assignee.all()
                assignee_list = task_table.process_user_list(
                                    task_obj.assignee.all())
                if params.get('logid') in assignee_list:
                    status = task_table.getStatus(task_obj.status)
                    data.append({'task_id': task_obj.id,
                                 'title': task_obj.title,
                                 'status': status,
                                 'admin_id': task_obj.admin_id,
                                 'assignee_id': assignee_list})
        print data
        # import pdb; pdb.set_trace()
        return HttpResponse(json.dumps(data), content_type='application/json')
