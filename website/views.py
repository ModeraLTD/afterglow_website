from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView, View
from .models import Service, Booking
from .forms import AvailabilityForm
from website.booking_functions.availability import check_availability

from . import serviceHtml

# Resets basket when you visit the main page
debugBasket = False

# Regular pages

def index(request):
    if debugBasket:
        del request.session['basket']

    basketIfNotExists(request)
    return render(request, "index.html")

def store(request):
    basketIfNotExists(request)
    services = Service.objects.all()

    # format twice for button
    # if prod is in basket
    products = serviceHtml.groupProds([
        serviceHtml.formatProduct(i, request)
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


def basket(request):
    items, totalPrice, totaltime = getBasketFormatted(request)
    formattime = serviceHtml.formatTime(totaltime)

    context = {
        "basket": items,
        "totalPrice": totalPrice,
        "totaltime": formattime
    }

    return render(
        request,
        "basket.html",
        context
    )


# POST/GET routes

def clearAllServices(request):
    """Clear all services in basket"""
    request.session['basket'] = []
    return HttpResponse(status=200)

def getTotalPrice(request):
    """Return the total basket price"""
    totalPrice = 0

    for item in request.session['basket']:
        try:
            prod = Service.objects.filter(prodID__exact=item)[0]
            totalPrice += prod.price
        except Exception as e:
            print(str(e))
    
    print("totalPrice", totalPrice)
    
    return HttpResponse(totalPrice)
def getTotalTime(request): 
    """Return total time for the basket"""
    totaltime = 0
    for item in request.session['basket']: 
        try: 
            prod = Service.objects.filter(prodID__exact = item)[0]
            totaltime += prod.time 
        except Exception as e:
            print(str(e))


def toggleBasket(request):
    """Toggles a service to the user's basket"""
    params = request.GET.dict()

    if 'id' not in params.keys():
        return HttpResponse("No id", status=400)
    if len(request.session['basket']) >= 30:
        return HttpResponse("Max items in basket", status=400)
    
    id_ = params['id']
    availableIDs = [i.prodID for i in Service.objects.all()]

    if id_ not in availableIDs:
        return HttpResponse("Invalid ID", status=400)
    
    if id_ in request.session['basket']:
        request.session['basket'].remove(id_)
        resp = "Removed from basket"
    else:
        request.session['basket'].append(id_)
        resp = "Added to basket"
    
    request.session.modified = True

    print(request.session['basket'])

    return HttpResponse(resp)

def isInBasket(request):
    """Fails if an id is not in basket atleast once"""
    params = request.GET.dict()

    if 'id' not in params.keys():
        return HttpResponse("No id", status=400)
    
    id_ = params['id']
    
    return HttpResponse({
        "exists": inBasket(id_),
    })

# Other

def getBasketFormatted(request):
    """Get a nicely formatted basket JSON object
       and also the total price."""
    
    totalPrice = 0
    items = []
    totaltime = 0

    for item in request.session['basket']:
        try:
            prod = Service.objects.filter(prodID__exact=item)[0]

            items.append({
                "prodID": prod.prodID,
                "name": prod.name,
                "price": prod.price,
                "time": prod.time
            })

            totalPrice += prod.price
            totaltime += prod.time
        except Exception as e:
            print(str(e))

    return items, totalPrice, totaltime

def inBasket(prod):
    return prod in request.session['basket']

def basketIfNotExists(request):
    if 'basket' not in request.session:
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
            if check_availability(Service, data['time_from'], data['time_to']):
                available_service.append(serv)
        if len(available_service) > 0:
            serv = available_service[0]
            
            booking = Booking.objects.create(
                user = self.request.user,
                Service = serv,
                Time_From = data['time_from'],
                Time_To = data['time_to']
            )
            booking.save()
            return HttpResponse(booking)
        else:
            return HttpResponse("This is not available")
            
                