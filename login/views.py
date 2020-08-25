from django.shortcuts import render, redirect
from .models import *
from quaranthings.models import *
import bcrypt
from django.contrib import messages

# Create your views here.
def index(request):
    if 'logged_user' in request.session:
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        total_quantity = 0
        if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
            order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
            for item in order_items:
                total_quantity += item.quantity
        context = {
            'user': user,
            'cart_count': total_quantity
        }
        return render(request, 'home.html', context)
    else:
        context = {
            'cart_count': 0
        }
        return render(request, 'home.html', context)

def login(request):
    if 'logged_user' in request.session:
        return redirect('/')
    else:
        context = {
            'cart_count': 0
        }
        return render(request, 'login.html', context)

def register(request):
    if 'logged_user' in request.session:
        return redirect('/')
    else:
        context = {
            'cart_count': 0
        }
        return render(request, 'register.html', context)

def process_register(request):
    if request.method == "GET":
        return redirect('/register')
    else:
        if 'logged_user' in request.session:
            return redirect('/')
        else:
            errors = User.objects.register_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/register') 
            else:
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], birthdate = request.POST['birthday'], email=request.POST['email'].lower(), password=pw_hash)
                request.session['logged_user'] = User.objects.all().last().email
                request.session['first_name'] = User.objects.all().last().first_name
                return redirect('/') 

def process_login(request):
    if request.method == "GET":
        return redirect('/login')
    else:
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login') 
        else:
            lower_email = request.POST['email'].lower()
            request.session['logged_user'] = User.objects.filter(email = lower_email).first().email
            request.session['first_name'] = User.objects.filter(email = lower_email).first().first_name
            return redirect('/') 


def logout(request):
    if 'logged_user' in request.session:
        del request.session['logged_user']
    return redirect('/')

def edit_profile(request):
    if 'logged_user' in request.session:
        user = User.objects.filter(email = request.session['logged_user']).all().first()
        total_quantity = 0
        if Order.objects.filter(user = user).filter(ordered = False).all().count() > 0:
            order_items = Order.objects.filter(user = user).filter(ordered = False).all().first().products.all()
            for item in order_items:
                total_quantity += item.quantity
        context = {
            'user': user,
            'cart_count':total_quantity
        }
        return render(request, 'edit_profile.html', context)
    else:
        return redirect('/login')

def process_profile_edit(request):
    if request.method == "POST":
        print(request.FILES)
        if request.POST['old_pw'] != "" or request.POST['new_pw'] != "" or request.POST['new_pw_conf'] != "":
            errors = User.objects.password_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/edit_profile') 
            else:
                user = User.objects.filter(email = request.session['logged_user']).first()
                if len(request.FILES) > 0:
                    for image in request.FILES.getlist('image'):
                        user.profile_picture = image
                password = request.POST['new_pw']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                user.password = pw_hash
                return redirect('/') 
        if len(request.FILES) > 0:
            print("getting here")
            user = User.objects.filter(email = request.session['logged_user']).all().first()
            user.profile_picture = request.FILES.getlist('image')[0]
            user.save()
            return redirect('/')
        return redirect('/')
    else:
        return redirect('/edit_profile')
