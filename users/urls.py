from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.quarangivers),
    path('/<int:id>', views.quarangiver),
    path('/cart', views.shopping_cart),
    path('/remove_cart_item', views.remove_cart_item),
    path('/update_cart_count', views.update_cart_count),
    path('/cart/process_order', views.process_order),
    path('/my_orders', views.my_orders)
]