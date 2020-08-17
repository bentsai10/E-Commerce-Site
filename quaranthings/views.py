from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Avg, Q
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
            quaranthing = Product.objects.create(name = request.POST['name'], description = request.POST['description'], price = request.POST['price'], stock = request.POST['stock'], seller = User.objects.filter(email = request.session['logged_user']).all().first(), views = 0)
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
    try:
        quaranthing = Product.objects.get(id = num)
        category = Product.objects.get(id = num).categories.all().first()
        quaranthing.views += 1
        quaranthing.save()
        if Review.objects.filter(product = Product.objects.get(id = num)).all().count() > 0:
            average_rating = Review.objects.filter(product = Product.objects.get(id = num)).all().aggregate(Avg('rating'))['rating__avg']
            rounded_rating = round(average_rating)
        else:
            rounded_rating = 0
        context = {
            'quaranthing': quaranthing,
            'related_things': category.products.all(),
            'average_rating': rounded_rating
        }
        return render(request, 'quaranthing.html', context)
    except User.DoesNotExist:
        return redirect('/')
    
def process_review(request):
    if request.method == 'POST':
        thing_id = request.POST['thing_id']
        product = Product.objects.get(id = thing_id)    
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        Review.objects.create(rating = request.POST['rating'], content = request.POST['content'], user = user, product = product)
        average_rating = Review.objects.filter(product = product).all().aggregate(Avg('rating'))['rating__avg']
        rounded_rating = round(average_rating)
        context = {
            'quaranthing': product,
            'average_rating': rounded_rating
        }
        return render(request, 'partials/review_section.html', context)
    return redirect('/')


def delete_review(request, num):
    if request.method == 'POST':    
        review = Review.objects.get(id = request.POST['review_id'])
        review.delete()
        product = Product.objects.get(id = num)   
        average_rating = Review.objects.filter(product = product).all().aggregate(Avg('rating'))['rating__avg']
        rounded_rating = round(average_rating)
        context = {
            'quaranthing': product,
            'average_rating': rounded_rating
        }
        return render(request, 'partials/review_section.html', context)
    else:
        return redirect('/quaranthings/{}'.format(num))

def delete_quaranthing(request, num):
    if request.method == 'POST':
        quaranthing = Product.objects.get(id = num)
        quaranthing.delete()
    return redirect('/')

def top_picks(request):
    context = {
        'picks': Product.objects.all().order_by('-views')[:40], 
        'categories': Category.objects.all()
    }
    return render(request, 'top_picks.html', context)

def category(request, category):
    formatted_category = category.title()
    if Category.objects.filter(name = formatted_category).all().count() < 1:
        return redirect('/')
    else:
        context = {
            'category': Category.objects.filter(name = formatted_category).all().first(),
            'products': Category.objects.filter(name = formatted_category).all().first().products.all()
        }
        return render(request, 'category.html', context)

def update_rating_subtitle(request, num):
    product = Product.objects.get(id = num)
    average_rating = Review.objects.filter(product = product).all().aggregate(Avg('rating'))['rating__avg']
    rounded_rating = round(average_rating)
    context = {
        'quaranthing': product,
        'average_rating': rounded_rating
    }
    return render(request, 'partials/rating_subtitle.html', context)

def update_review_header(request, num):
    product = Product.objects.get(id = num)
    average_rating = Review.objects.filter(product = product).all().aggregate(Avg('rating'))['rating__avg']
    rounded_rating = round(average_rating)
    context = {
        'quaranthing': product,
        'average_rating': rounded_rating
    }
    return render(request, 'partials/review_header.html', context)

category_tags = ["food", "catch_up", "games", "exercise", "random_fun", "wearables", "other"]

#arrays of category id pertinent to specific category tag
tag_to_category_id = {
    "food":[1, 2, 3, 4, 21],
    "catch_up":[5,  6, 12],
    "games": [9, 13],
    "exercise": [8,  11],
    "random_fun" : [ 7,  10, 14],
    "wearables" : [15, 17, 18], 
    "other": [16, 19, 20]
}


def filter_tp(request):
    if request.method == "POST":
        print(request.POST)
        chosen_categories = []
        for tag in category_tags:
            if tag in request.POST:
                for category_id in tag_to_category_id[tag]:
                    chosen_categories.append(category_id)
        if len(chosen_categories) == 0:
            filtered_tp = Product.objects.all()
        else:
            filtered_tp = Product.objects.filter(categories__in = chosen_categories).all()
        min = float(request.POST['min']) if request.POST['min'] != '' else 0
        max = float(request.POST['max']) if request.POST['max'] != '' else 10000
        filtered_tp = filtered_tp.filter(price__lte = max, price__gte = min)
        context = {
            'picks': filtered_tp.order_by("-views")[:40]
        }
        return render(request, 'partials/filtered_top_picks.html', context)
    else:
        redirect('/quaranthings/top_picks')
