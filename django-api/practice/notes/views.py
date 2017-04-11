from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, RequestContext
from django import forms
from django.shortcuts import redirect, render_to_response

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import Note, NoteForm
from django.forms.models import modelformset_factory


class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


@login_required(login_url='/notes/index/')
def dashboard(request):
    from django.forms.models import inlineformset_factory
    noteformset = inlineformset_factory(User, Note, can_delete=True, 
                                        fields='__all__', extra=1)
    if request.method == 'POST':
        formset = noteformset(request.POST, request.FILES,
                              instance=request.user)
        if formset.is_valid():
            formset.save()
        return redirect('dashboard')
    else:
        formset = noteformset(instance=request.user)
        # import pdb;pdb.set_trace()
        return render_to_response(
            'dashboard.html',
            {'form': NoteForm(), 'formset': formset}, RequestContext(request))


@login_required(login_url='/notes/index/')
def old_dashboard(request):
    if request.method == 'POST':
        tmp = request.POST.copy()
        tmp.update({'owner': request.user.id})
        form = NoteForm(tmp)
        if not form.is_valid():
            template = loader.get_template('dashboard.html')
            rc = RequestContext(request, {'form': form})
            return HttpResponse(template.render(rc))
        note = form.save(commit=False)
        note.owner = request.user
        note.save()
        return redirect('dashboard')
    else:
        template = loader.get_template('dashboard.html')
        rc = RequestContext(request, {'form': NoteForm()})
        return HttpResponse(template.render(rc))


def dologout(request):
    logout(request)
    return redirect('index')


def index(request):
    # return HttpResponse("Hello, World!")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if not username or not password:
                return HttpResponse('Error')
            try:
                user = User.objects.get(username=username)
            except Exception as ex:
                print "Creating user....", username
                user = User.objects.create_user(username, username, password)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                template = loader.get_template('index.html')
                rc = RequestContext(request, {'fruits': ['CK', 'Mango', 'Apple'],
                                              'form': form})
                return HttpResponse(template.render(rc))
            return redirect('dashboard')
        else:
            template = loader.get_template('index.html')
            rc = RequestContext(request, {'fruits': ['CK', 'Mango', 'Apple'],
                                          'form': form})
            return HttpResponse(template.render(rc))
    else:
        template = loader.get_template('index.html')
        rc = RequestContext(request, {'fruits': ['CK', 'Mango', 'Apple'],
                                      'form': LoginForm()})
        return HttpResponse(template.render(rc))


