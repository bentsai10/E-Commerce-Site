from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Avg
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
            return redirect('/quaranthings/{}'.format(quaranthing.id))

def quaranthing(request, num):
    category = Product.objects.get(id = num).categories.all().first()
    average_rating = Review.objects.filter(product = Product.objects.get(id = num)).all().aggregate(Avg('rating'))['rating__avg']
    context = {
        'quaranthing': Product.objects.get(id = num),
        'related_things': category.products.all(),
        'average_rating': average_rating
    }
    return render(request, 'quaranthing.html', context)

def process_review(request, num):
    if request.method == 'POST':    
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        Review.objects.create(rating = request.POST['rating'], content = request.POST['content'], user = user, product = Product.objects.get(id = num))
    return redirect('/quaranthings/{}'.format(num))


def delete_review(request, num):
    if request.method == 'POST':    
        review = Review.objects.get(id = request.POST['review_id'])
        review.delete()
    return redirect('/quaranthings/{}'.format(num))

