from django.http import HttpResponse
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView
from .models import service, Booking
from .forms import AvailabilityForm
from website.booking_functions.availability import check_availability
# Create your views here.
def index(request):
    return render(request, "index.html")

class serviceList(ListView):
    model = service




class bookingList(ListView):
    model = Booking

class BookingView(FormView):
    form_class =AvailabilityForm
    template_name = 'availability_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        service_list = service.objects.filter(category=data['service_category'])
        available_service = []
        for serv in service_list:
            if check_availability(service, data['bookin'], data['bookout']):
                available_service.append(serv)
        if len(available_service) > 0:
            serv = available_service[0]
            
            booking = Booking.objects.create(
                user = self.request.user,
                Service = serv,
                bookin = data['bookin'],
                bookout = data['bookout']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse("This is not available")
            
                