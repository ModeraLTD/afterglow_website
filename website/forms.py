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
    
        def clean_date(self):
            day = self.cleaned_data['date']
            if day <= date.today():
                raise forms.ValidationError('Date should be upcoming (tomorrow or later)', code='invalid')
        def clean_time(self):
            Time_From = self.cleaned_data['Time_From']
            time_list = Available_Day.time_list
            roundedtime = round(views.getTotalSlot_Time.totalSlotTime2)
            totaltime = roundedtime + views.getTotalSlot_Time.totalSlotTime
            if Time_From in time_list:
                #Checking if the next time slots are available
                for i in range(totaltime):
                    check_next_slot = Booking.Time_From + i 
                    if check_next_slot not in time_list:
                        raise ValidationError("Your sessions overruns other bookings! you cannot choose this time", code = 'invalid')
                #If not then it will remove the time slots from the list
                if views.getTotalSlot_Time.totalSlotTime2 != 0:
                    numberdec = (views.getTotalSlot_Time.totalSlotTime2 / 0.5) - 1
                else: 
                    numberdec = 0
                remove_slot = Booking.Time_From + views.getTotalSlot_Time.totalSlotTime + numberdec
                for v in range(Booking.Time_From, remove_slot + 1):
                    time_list.remove(v)
            else:
                raise ValidationError("This booking time is not available!" , code = "invalid")
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
    
    