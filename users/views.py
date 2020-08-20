from django.shortcuts import render
from .models import *
from login.models import *
from quaranthings.models import *
from django.db.models import Q

# Create your views here.

def quarangivers(request):
    user = User.objects.filter(email = request.session['logged_user']).all().first()
    total_quantity = 0
    if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
        order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
        for item in order_items:
            total_quantity += item.quantity
    context = {
        'user': User.objects.filter(email = request.session['logged_user']).all().first(),
        'quarangivers': User.objects.all(),
        'cart_count': total_quantity
    }
    return render(request, 'quarangivers.html', context)

def quarangiver(request, id):
    user = User.objects.filter(email = request.session['logged_user']).all().first()
    total_quantity = 0
    if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
        order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
        for item in order_items:
            total_quantity += item.quantity
    context = {
        'user': user,
        'quarangiver': User.objects.get(id = id), 
        'cart_count': total_quantity
    }
    return render(request, 'quarangiver.html', context)

def shopping_cart(request):
    if 'logged_user' not in request.session:
        return redirect('/login')
    else:
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        total_quantity = 0
        if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
            order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
            for item in order_items:
                total_quantity += item.quantity
        context = {
            'user': user,
            'cart': Order.objects.filter(user = user).filter(ordered = False).all().first(),
            'cart_count': total_quantity
        }
        return render(request, 'cart.html', context)
