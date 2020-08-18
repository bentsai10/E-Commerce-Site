from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.quarangivers),
    path('/<int:id>', views.quarangiver)
]