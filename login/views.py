from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

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