from django.urls import path
from django.urls.resolvers import URLPattern

from . import views
from .views import serviceList, BookingView
from .views import bookingList
app_name = "website"
urlpatterns = [
    path("", views.index, name="index"),
    path('service_list', serviceList.as_view(), name = "serviceList"),
    path('booking_list', bookingList.as_view(), name = "BookingList"),
    path('book/', BookingView.as_view(), name = 'booking_view')
]