from django.urls import path, include
from . import views

urlpatterns = [
    path('/new', views.new_quaranthing),
    path('/process_new_quaranthing', views.process_new_quaranthing)
]
