from django.shortcuts import render, redirect, HttpResponse
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
        return redirect('/quaranthings/new')
    else:
        print('user uploaded', len(request.FILES), 'files')
        print(request.FILES.getlist('image'))
        errors = Product.objects.validator(request.POST, request.FILES)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quaranthings/new')
        else:
            quaranthing = Product.objects.create(name = request.POST['name'], description = request.POST['description'], price = request.POST['price'], stock = request.POST['stock'], seller = User.objects.filter(email = request.session['logged_user']).all().first())
            for key in request.POST.keys():
                print(key)
            if request.POST['thing_type'] == 'activity':
                for category in Category.objects.filter(category_type = 'activity').all():
                    if category.name in request.POST:
                        quaranthing.categories.add(category)
            else:
                for category in Category.objects.filter(category_type = 'DIY Item').all():
                    if category.name in request.POST:
                        quaranthing.categories.add(category)
            for image in request.FILES.getlist('image'):
                img = Image.objects.create(img_file = image)
                img.products.add(quaranthing)
            return redirect('/')