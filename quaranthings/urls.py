from django.urls import path, include
from . import views

urlpatterns = [
    path('/new', views.new_quaranthing),
]