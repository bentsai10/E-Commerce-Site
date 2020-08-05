from django.shortcuts import render, redirect

# Create your views here.

def new_quaranthing(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    else:
        return render(request, 'new_quaranthing.html')