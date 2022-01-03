from django import forms   
from django.forms import ModelForm
from .models import Booking, Customer, Available_Day, Service
from datetime import date
from . import views
from django.core.exceptions import ValidationError

class BookingForm(ModelForm):
    class Meta: 
        model = Booking
        exclude = [ 'uuid']
        def clean_Time_From(self):
            Time_From = self.cleaned_data.get['Time_From']
            time_list = Available_Day.time_list
            roundedtime = round(views.getTotalSlot_Time.totalSlotTime2)
            totaltime = roundedtime + views.getTotalSlot_Time.totalSlotTime
            if Time_From in time_list:
                #Checking if the next time slots are available
                for i in range(totaltime):
                    check_next_slot = Booking.Time_From + i 
                    if check_next_slot not in time_list:
                        raise forms.ValidationError("Your sessions overruns other bookings! you cannot choose this time", code = 'invalid')
                #If not then it will remove the time slots from the list
                return Time_From
            else:
                raise forms.ValidationError("This booking time is not available!" , code = "invalid")
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        
        fields = '__all__'
    
    