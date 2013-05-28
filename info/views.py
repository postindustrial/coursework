# Create your views here.
# -*- coding: utf-8 -*-



from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from django.conf import settings
from django.http import QueryDict
from django.utils.datastructures import SortedDict
from django.db.models import Q
from info.models import Schedule, Settings, Group

from social_auth import __version__ as version
from social_auth.utils import setting

import datetime

def get_current_week():
    today = datetime.datetime.today()
    delta_days = (today - settings.SEMESTER_BEGIN).days
    current_week = 2 - (delta_days / 7) % 2 # семестр начался со второй недели
    return current_week

def frontpage(request):
    if request.user.is_authenticated():
        return redirect('info.views.home')
    else:
        return redirect('info.views.selected_schedule')

def home(request):
    if request.user.is_authenticated():
        current_week = get_current_week()
        current_weekday = datetime.datetime.today().weekday()
        user = request.user
        user_group = user.group
        temp = Settings.objects.filter(student__email=user.email)
        personal_schedule = Schedule.objects.all().\
            filter(course__group__name=user_group).\
            order_by('begin_time')#.exclude(pk__in=temp)
        for element in temp.all():
            personal_schedule = personal_schedule.exclude(pk=element.schedule_id)
        if current_weekday == 6:# воскресенье
            personal_schedule = personal_schedule.filter(weekday=0). \
                filter(week=3-current_week)
        else:
            personal_schedule = personal_schedule.filter(weekday__in=[current_weekday, current_weekday + 1]). \
                filter(week=current_week)
        context = {'personal_schedule_current': personal_schedule}
        return render(request, 'home.html', context)
    else:
        return redirect('info.views.selected_schedule')

def selected_schedule(request):
    context = {}
    selected_schedule = {}
    group_list = Group.objects.all()
    if request.method == 'POST':
        selected_group = request.POST['group']
        selected_schedule = Schedule.objects.all().filter(course__group__name=selected_group).order_by('begin_time')
    else:
        selected_group = Group.objects.get().name
        selected_schedule = Schedule.objects.all().filter(course__group__name=selected_group).order_by('begin_time')
    context = {'groups': group_list, 'selected_group': selected_group, 'selected_schedule': selected_schedule, 'week_number': range(1, 3)}
    return render(request, 'schedule.html', context)

def full_personal_schedule(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            user_group = request.user.group
            Settings.objects.filter(student__group=user_group).delete()
            personal_settings = request.POST.getlist('settings')
            for item in personal_settings:
                schedule_item=Schedule.objects.get(pk=int(item))
                new_settings = Settings(student=request.user, schedule=schedule_item)
                new_settings.save()
        user_group = request.user.group
        personal_schedule = Schedule.objects.all().filter(course__group__name=user_group).order_by('begin_time')
        context = {'personal_schedule_full': personal_schedule, 'week_number': range(1, 3)}
        return render(request, 'full.html', context)
    else:
        return redirect('info.views.selected_schedule')


@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('done.html', ctx, RequestContext(request))


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form.html', {}, RequestContext(request))


def form2(request):
    context = Group.objects.all()
    if request.method == 'POST' and request.POST.get('group'):
        request.session['saved_group'] = request.POST['group']
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form2.html', {}, RequestContext(request, {'groups': context}))


def close_login_popup(request):
    return render_to_response('close_popup.html', {}, RequestContext(request))
