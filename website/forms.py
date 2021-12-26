from django import forms   

class AvailabilityForm(forms.Form):
    Date = forms.DateField(required= True, input_formats=["%Y-%m-%d"])
    Time_From = forms.TimeField(required= True, input_formats=["%H:%M"])
    first_Name = forms.CharField(required = True,max_length=16)
    last_Name = forms.CharField(required = True, max_length = 15)
    email = forms.CharField(required = True, max_length = 20)
    phone = forms.CharField(required = True, max_length = 11)
    POSTCODE = forms.CharField(required = True, max_length = 8)
    address = forms.CharField(required = True, max_length = 20)
    city = forms.CharField(required = True, max_length = 10)
    county = forms.CharField(max_length = 20)
    