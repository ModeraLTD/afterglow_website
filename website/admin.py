from django.contrib import admin
# Register your models here.
from .models import service, Booking

admin.site.register(service)
admin.site.register(Booking)