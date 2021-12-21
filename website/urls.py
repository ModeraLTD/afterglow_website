from django.urls import path
from django.urls.resolvers import URLPattern

from . import views
from .views import ServiceList, BookingView
from .views import BookingList
app_name = "website"
urlpatterns = [
    path("", views.index, name="index"),
    path('service_list', ServiceList.as_view(), name = "serviceList"),
    path('booking_list', BookingList.as_view(), name = "BookingList"),
    path('book/', BookingView.as_view(), name = 'booking_view')
]