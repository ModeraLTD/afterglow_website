from django.http import HttpResponse
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView
from .models import Service, Booking
from .forms import AvailabilityForm
from website.booking_functions.availability import check_availability

import json

from . import serviceHtml

# Create your views here.

def index(request):
    return render(request, "index.html")

def store(request):
    services = Service.objects.all()

    products = serviceHtml.groupProds([
        serviceHtml.formatProduct(i)
        for i in services
    ])

    helpTexts = dict([(i.name, i.description) for i in services])

    context = {
        "SKIN": products["SKIN"],
        "HEALTH": products["HEALTH"],
        "NON_INV": products["NON_INV"],
        "APP": products["APP"],
        "help": helpTexts,
    }

    for k, v in context.items():
        print(k, "\n".join(v), "\n\n\n")

    return render(
        request, 
        "store.html",
        context
    )

class ServiceList(ListView):
    model = Service


class BookingList(ListView):
    model = Booking

class BookingView(FormView):
    form_class =AvailabilityForm
    template_name = 'availability_form.html'
    
    def form_valid(self, form):
        data = form.cleaned_data
        service_list = Service.objects.filter(category=data['service_category'])
        available_service = []
        for serv in service_list:
            if check_availability(Service, data['bookin'], data['bookout']):
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
            
                