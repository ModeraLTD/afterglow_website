from django.contrib import admin

# Register your models here.
from .models import Service, Booking, Customer

admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Customer)