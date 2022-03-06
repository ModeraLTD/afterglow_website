from django import forms   
from django.forms import ModelForm
from .models import Booking, Customer, Available_Day, Service
from datetime import date
from . import views
from django.core.exceptions import ValidationError

from . import views
from django.core.exceptions import ValidationError

class BookingForm(ModelForm):
    class Meta: 
        model = Booking
        exclude = [ 'uuid']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        
        fields = '__all__'