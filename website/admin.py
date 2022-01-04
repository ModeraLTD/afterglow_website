from django.contrib import admin

# Register your models here.
from .models import Service, Booking, Customer, Order, Available_Day, orderItem

admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Available_Day)
admin.site.register(orderItem)