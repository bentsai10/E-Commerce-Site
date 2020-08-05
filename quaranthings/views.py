from django.shortcuts import render, redirect

# Create your views here.

def new_quaranthing(request):
    return render(request, 'new_quaranthing.html')