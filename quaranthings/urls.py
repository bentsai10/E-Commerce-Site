from django.urls import path, include
from . import views

urlpatterns = [
    path('/new', views.new_quaranthing),
    path('/process_new_quaranthing', views.process_new_quaranthing),
    path('/<int:num>', views.quaranthing),
    path('/<int:num>/process_review', views.process_review),
    path('/<int:num>/delete_review', views.delete_review),
    path('/<int:num>/delete_quaranthing', views.delete_quaranthing),
    path('/top_picks', views.top_picks),
    path('/<str:category>', views.category)
]
