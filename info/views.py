# Create your views here.

from django.shortcuts import render
from info.models import Schedule

def index(request):
    context = {'schedule_all': Schedule.objects.all()}
    return render(request, 'frontpage.html', context)