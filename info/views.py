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
from info.models import Schedule

from social_auth import __version__ as version
from social_auth.utils import setting

import datetime
from dateutil.relativedelta import relativedelta


def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('done')
    else:
        return render_to_response('frontpage.html', {'version': version},
                                  RequestContext(request))

def get_current_week():
    today = datetime.datetime.today()
    delta_days = (today - settings.SEMESTER_BEGIN).days
    current_week = 1 + (delta_days / 7) % 2 # семестр начался со второй недели
    return current_week

def index(request):
    if request.user.is_authenticated():
        current_week = get_current_week()
        current_weekday = datetime.datetime.today().weekday()
        user_group = request.user.group
        context = {'schedule_personal': Schedule.objects.all().filter(course__group__name=user_group).filter(weekday__in=[current_weekday, current_weekday + 1]).filter(week=current_week).order_by('begin_time')}
        return render(request, 'frontpage.html', context)
    else:
        return render(request, 'frontpage.html')

def full_schedule(request):
    user_group = request.user.group
    user_id = request.user.email
    context = {'schedule_full':Schedule.objects.all().filter(course__group__name=user_group).order_by('begin_time'), 'week_number': range(1, 3), 'day_number': range(0, 6)}
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
    if request.method == 'POST' and request.POST.get('first_name'):
        request.session['saved_first_name'] = request.POST['first_name']
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form2.html', {}, RequestContext(request))


def close_login_popup(request):
    return render_to_response('close_popup.html', {}, RequestContext(request))
