from django.urls import path
from django.urls.resolvers import URLPattern

from . import views
from .views import ServiceList, BookingFormView, BookingList, CustomerFormView, BookingFormView3 

app_name = "website"

urlpatterns = [
    path("", views.index, name="index"),
    path("store", views.store, name="store"),
    path("basket", views.basket, name="basket"),
    path("basket/toggle", views.toggleBasket, name="toggleBasket"),
    path("basket/getTotalPrice", views.getTotalPrice, name="getTotalPrice"),
    path("basket/clearAll", views.clearAllServices, name="clearAll"),
    path('service_list', ServiceList.as_view(), name = "serviceList"),
    path('booking_list', BookingList.as_view(), name = "BookingList"),
    path('customer', CustomerFormView.as_view(), name = "customer_form"),
    path('customer/booking', BookingFormView3.as_view(), name = 'booking_view'),
    path('customer/book/payment', views.payment, name = "payment"),
    path('complete/', views.completeOrder, name = "complete")
]