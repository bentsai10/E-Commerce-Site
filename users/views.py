from django.shortcuts import render
from .models import *
from login.models import *
from quaranthings.models import *
from django.db.models import Q

# Create your views here.

def quarangivers(request):
    context = {
        'user': User.objects.filter(email = request.session['logged_user']).all().first(),
        'quarangivers': User.objects.all()
    }
    return render(request, 'quarangivers.html', context)

def quarangiver(request, id):
    context = {
        'user': User.objects.filter(email = request.session['logged_user']).all().first(),
        'quarangiver': User.objects.get(id = id)
    }
    return render(request, 'quarangiver.html', context)
