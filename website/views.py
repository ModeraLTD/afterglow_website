from django.http import HttpResponse
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView
from .models import Service, Booking
from .forms import AvailabilityForm
from website.booking_functions.availability import check_availability

from . import serviceHtml


# Regular pages

def index(request):
    basketIfNotExists(request)
    return render(request, "index.html")

def store(request):
    basketIfNotExists(request)
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

    return render(
        request, 
        "store.html",
        context
    )


# POST/GET routes

def addToBasket(request):
    """Adds a service to the user's basket"""
    params = request.GET.dict()

    if 'id' not in params.keys():
        return HttpResponse("No id", status=400)
    if len(request.session['basket']) >= 30:
        return HttpResponse("Max items in basket", status=400)
    
    id_ = params['id']
    availableIDs = [i.name for i in Service.objects.all()]

    if id_ not in availableIDs:
        return HttpResponse("Invalid ID", status=400)
    
    if id_ in request.session['basket']:
        return HttpResponse("Already in basket", status=400)

    request.session['basket'].append(id_)
    request.session.modified = True

    return HttpResponse(status=204)

def isInBasket(request):
    """Fails if an id is not in basket atleast once"""
    params = request.GET.dict()

    if 'id' not in params.keys():
        return HttpResponse("No id", status=400)
    
    id_ = params['id']
    
    return HttpResponse({
        "exists": id_ in request.session['basket']
    })

# Other

def basketIfNotExists(request):
    if 'basket' not in request.session or True:
        request.session['basket'] = []


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
            
                