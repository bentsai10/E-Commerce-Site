from django.shortcuts import render, redirect
from .models import *
from login.models import *
from django.contrib import messages

# Create your views here.

def new_quaranthing(request):
    context = {
        'activity_categories':Category.objects.filter(category_type = 'activity').all(),
        'diy_categories': Category.objects.filter(category_type = 'DIY Item').all()
    }
    return render(request, 'new_quaranthing.html', context)

def process_new_quaranthing(request):
    if request.method == "GET":
        redirect('/quaranthings/new')
    else:
        errors = Product.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            redirect('/quaranthings/new')
        else:
            Product.objects.create()