from django import forms   

class AvailabilityForm(forms.Form):
    SERVICE_CATEGORIES = {
        ('Face', "Full Face"),
        ('Body', "Full body"),
        ('Pack', "Full packages")
    }
    
    service_category = forms.ChoiceField(choices = SERVICE_CATEGORIES, required = True)
    
    bookin = forms.DateTimeField(required= True, input_formats=["%Y-%m-%dT%H:%M"])
    bookout = forms.DateTimeField(required= True, input_formats=["%Y-%m-%dT%H:%M"])