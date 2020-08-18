from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('process_login', views.process_login),
    path('register', views.register),
    path('process_register', views.process_register),
    path('logout', views.logout),
    path('edit_profile', views.edit_profile),
    path('process_profile_edit', views.process_profile_edit)
]