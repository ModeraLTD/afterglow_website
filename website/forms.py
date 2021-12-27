from django import forms   
from django.forms import ModelForm
from .models import Booking, Customer

class BookingForm(ModelForm):
    class Meta: 
        model = Booking
        fields = '__all__'
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        
        fields = '__all__'
#class AvailabilityForm(forms.Form):
    #Date = forms.DateField(required= True, input_formats=["%Y-%m-%d"])
    #Time_From = forms.TimeField(required= True, input_formats=["%H:%M"])


#class CustomerForm(forms.Form):
    #fullname = forms.CharField(required = True,max_length=30)
    #email = forms.CharField(required = True, max_length = 20)
    #phone = forms.CharField(required = True, max_length = 11)
    #POSTCODE = forms.CharField(required = True, max_length = 8)
    #address = forms.CharField(required = True, max_length = 20)
    
    