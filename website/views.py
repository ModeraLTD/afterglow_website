from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.views.generic import ListView, FormView, View, TemplateView
from .models import Service, Booking, Customer, Order
from .forms import BookingForm, CustomerForm
from website.booking_functions.availability import check_availability
import stripe
from django.conf import settings
from . import serviceHtml
from django.db import models
import random
stripe.api_key = settings.STRIPE_SECRET_KEY

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


def getTotalSlot_Time(request): 
    """Return total slot_time for the basket"""
    totalSlotTime = 0
    for item in request.session['basket']: 
        try: 
            prod = Service.objects.filter(prodID__exact = item)[0]
            totalSlotTime += prod.slot_time 
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
        

class CustomerFormView(FormView):
    template_name = 'test_form2.html'
    def get(self, request): 
        form = CustomerForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            c = form.save()
            new_customer = c.clean()
            request.session['customer'] = new_customer
            return HttpResponseRedirect('customer/book')
        args = {'form': form}
        return render(request, self.template_name, args)

def success(request): 
    return render(request, 'success.html')  

class BookingView(FormView):
    template_name = 'test_form.html'
    def get(self, request): 
        form = BookingForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        import uuid
        form = BookingForm(request.POST)
        if form.is_valid():
            b = form.save()
            new_booking = b.clean()
            request.session['new_booking'] = new_booking
            return HttpResponseRedirect('book/success')
        args = {'form': form}
        return render(request, self.template_name, args)
  
def payment(self, request): 
    
    
    self.Order.customer = request.session['customer']
    self.Order.booking = request.session['new_booking']
    
        
    
 
            
                