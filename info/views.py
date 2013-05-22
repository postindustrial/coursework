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
from django.db.models import Q
from info.models import Schedule, Settings

from social_auth import __version__ as version
from social_auth.utils import setting

import datetime

def get_current_week():
    today = datetime.datetime.today()
    delta_days = (today - settings.SEMESTER_BEGIN).days
    current_week = 1 + (delta_days / 7) % 2 # семестр начался со второй недели
    return current_week

def frontpage(request):
    if request.user.is_authenticated():
        return redirect('info.views.home')
    else:
        return render(request, 'frontpage.html')

def home(request):
    if request.user.is_authenticated():
        current_week = get_current_week()
        current_weekday = datetime.datetime.today().weekday()
        user_group = request.user.group
        personal_schedule = Schedule.objects.all().filter(course__group__name=user_group).filter(weekday__in=[current_weekday, current_weekday + 1]).filter(week=current_week).order_by('begin_time')
        personal_schedule = personal_schedule.filter(~Q(pk__in=Settings.objects.filter(schedule__course__group__name=user_group)))
        context = {'personal_schedule_current': personal_schedule}
        return render(request, 'home.html', context)
    else:
        return render(request, 'frontpage.html')

def full_schedule(request, group_number="356"):
    group_list = Group.objects.all()
    context = {'group_list': group_list}
    return render(request, 'schedule.html', context)

def full_personal_schedule(request):
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
    context = {'personal_schedule_full': personal_schedule, 'week_number': range(1, 3), 'day_number': range(0, 6)}
    return render(request, 'full.html', context)


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
    if request.method == 'POST' and request.POST.get('group'):
        request.session['saved_group'] = request.POST['group']
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form2.html', {}, RequestContext(request))


def close_login_popup(request):
    return render_to_response('close_popup.html', {}, RequestContext(request))
