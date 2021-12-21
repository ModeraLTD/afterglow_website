from django.contrib import admin

# Register your models here.
from .models import Service, Booking

admin.site.register(Service)
admin.site.register(Booking)