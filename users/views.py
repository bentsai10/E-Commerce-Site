from django.shortcuts import render, redirect
from .models import *
from login.models import *
from quaranthings.models import *
from django.db.models import Q
from decimal import *

# Create your views here.

def quarangivers(request):
    context = {
        'quarangivers': User.objects.all()
    }
    if 'logged_user' in request.session:
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        total_quantity = 0
        if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
            order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
            for item in order_items:
                total_quantity += item.quantity
        context['user'] = user
        context['cart_count'] = total_quantity
    else:
        context['cart_count'] = 0
    return render(request, 'quarangivers.html', context)

def quarangiver(request, id):
    context = {
        'quarangiver': User.objects.get(id = id)
    }
    if 'logged_user' in request.session:
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        total_quantity = 0
        if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
            order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
            for item in order_items:
                total_quantity += item.quantity
        context['user'] = user
        context['cart_count'] = total_quantity
    else:
        context['cart_count'] = 0
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
        else:
            Order.objects.create(user = user, ordered = False, total = 0)
        context = {
            'user': user,
            'cart': Order.objects.filter(user = user).filter(ordered = False).all().first(),
            'cart_count': total_quantity,
            'total_price': Order.objects.filter(user = user).filter(ordered = False).all().first().total
        }
        return render(request, 'cart.html', context)

def remove_cart_item(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        cart = Order.objects.filter(user = user).filter(ordered = False).all().first()
        cart_item = OrderItem.objects.get(id = request.POST['cart_item_id']) 
        cart.total -= Decimal(cart_item.product.price) * Decimal(cart_item.quantity)
        cart.products.remove(cart_item)
        cart.save()
        total_quantity = 0
        if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
            order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
            for item in order_items:
                total_quantity += item.quantity
        context = {
            'user': user,
            'cart': cart,
            'cart_count': total_quantity,
            'total_price': cart.total
        }
        return render(request, 'partials/partial_cart.html', context)
    else:
        return redirect('/users/cart')

def update_cart_count(request):
    total_quantity = 0
    user = User.objects.filter(email = request.session['logged_user']).all().first()
    if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
        order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
        print(len(order_items))
        for item in order_items:
            total_quantity += item.quantity
    print(total_quantity)
    context = {
        'cart_count': total_quantity
    }
    return render(request, 'partials/update_cart_items.html', context)

def process_order(request):
    user = User.objects.filter(email = request.session['logged_user']).all().first()
    cart = Order.objects.filter(user = user).filter(ordered = False).all().first()
    cart.ordered = True
    cart.save()
    return redirect('/users/my_orders')

def my_orders(request):
    user = User.objects.filter(email = request.session['logged_user']).all().first()
    total_quantity = 0
    if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
        order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
        for item in order_items:
            total_quantity += item.quantity
    context = {
        'user': user,
        'cart_count': total_quantity,
        'orders': Order.objects.filter(user = user).filter(ordered = True).all()
    }
    return render(request, 'orders.html', context)

