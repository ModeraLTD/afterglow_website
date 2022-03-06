import django
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.views.generic import ListView, FormView, View, TemplateView
from .models import Available_Day, Service, Booking, Customer, Order, orderItem
from .forms import BookingForm, CustomerForm
from website.booking_functions.availability import check_availability
from django.conf import settings
from . import serviceHtml
from django.db import models
import random
from .models import TIMESLOT_LIST
import json
from .ID import OrderID
# Resets basket when you visit the main page
debugBasket = False
maxAvailableDays = 8

# Regular pages

def index(request):
    if debugBasket:
        del request.session['basket']

    basketIfNotExists(request)
    
    # render available days (up to maxAvailableDays = 8)
    days = Available_Day.objects.order_by("days")[:maxAvailableDays]

    context = {
        "days": [formatDay(i.days) for i in days],
    }
    
    return render(
        request,
        "index.html",
        context,
    )

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
    totalSlotTime2 = 0
    for item in request.session['basket']: 
        try: 
            prod = Service.objects.filter(prodID__exact = item)[0]
            if prod.slot_time == 0.5:
                totalSlotTime2 += prod.slot_time
            else:
                totalSlotTime += prod.slot_time 
        except Exception as e:
            print(str(e))
    
    return totalSlotTime, totalSlotTime2

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

def formatDay(day):
    """Format a day available into a nicely readable string

    Args:
        day (datetime.date): Day
    """
    def makeDayStr(d):
        lastDigit = int(str(d)[-1])
        if lastDigit == 1:
            ending = "st"
        elif lastDigit == 2:
            ending = "nd"
        elif lastDigit == 3:
            ending = "rd"
        else:
            ending = "th"
        
        return f"{d}{ending}"

    return day.strftime("%A {} %B %Y").format(makeDayStr(day.day))

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
        #if len(request.session['basket']) == 0:
            #return HttpResponseRedirect('') 
        form = CustomerForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            c = form.save()
            new_customer = c.clean()
            request.session['name'] = form.cleaned_data['fullname']
            request.session['email'] = form.cleaned_data['email']
            request.session['phone'] = form.cleaned_data['phone']
            return HttpResponseRedirect('customer/booking')
        args = {'form': form}
        return render(request, self.template_name, args) 


class BookingFormView(FormView):
    template_name = 'test_form.html'
    def get(self, request):
        form = BookingForm()
        return render(request, self.template_name, {'Available': Available_Day.objects.all()})
    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            b = form.save()
            return HttpResponseRedirect('customer/book/payment')
        args = {'form':form}
        return render(request, self.template_name, args) 
booking_array = []
class BookingFormView3(FormView): 
    template_name = 'test_form.html'
    def get(self, request):
        form = BookingForm()
        return render(request, self.template_name, {'Available': Available_Day.objects.all()})
    def post(self, request):
        form = BookingForm(request.POST)
        if form.is_valid():
            b = form.save()
            request.session['time'] = form.cleaned_data['Time_From']
            date = form.cleaned_data.get('date')
            time_list = date.time_list
            request.session['time_list'] = time_list
            date= date.days
            date = formatDay(date)
            request.session['date'] = date
            booking = Booking.objects.filter(uuid__exact = b.uuid)[0]
            booking_array.append(booking)
            return HttpResponseRedirect('book/payment')
        args = {'form':form, 'Available': Available_Day.objects.all()}
        return render(request, self.template_name, args)      

def payment(request): 
    try: 
        booking = booking_array[0]
        phone = request.session['phone']
    except: 
        return HttpResponseRedirect("basket")
    items, totalPrice, totaltime = getBasketFormatted(request)
    time = request.session['time']
    time = TIMESLOT_LIST[time][1]
    name = request.session['name']
    email = request.session['email']
    transaction_id = str(OrderID())
    first = request.session['name'][0]
    second = request.session['name'][1]
    date = request.session['date']
    transaction_id = first + second + transaction_id
    request.session['transaction_id'] = transaction_id
    context = { 'totalPrice': totalPrice, 
                'totalTime': totaltime,
                'name': name,
                'email': email,
                'transaction_id': transaction_id,
                'date' : date,}
                
    return render(request, 'payment.html', context)
from .paypal import PayPalClient
from .booking_slot import removeSlot
def complete_order(request):
    items, totalPrice, totaltime = getBasketFormatted(request)
    PPClient = PayPalClient()
    body = json.loads(request.body)
    data = body['transaction_id']
    request.session['data'] = data
    booking = booking_array[0]
    phone = request.session['phone']
    phone = request.session['phone']
    basket = request.session['basket']
    customer = Customer.objects.filter(phone__exact = phone)[0]
    order = Order.objects.create(
        customer = customer, booking = booking, billing_status = True, totalpaid = totalPrice
    )
    order_id = order
    for item in basket: 
        prod = Service.objects.filter(prodID__exact=item)[0]
        orderItem.objects.create(order = order, service = prod, transaction_id = data)
    time = request.session['time'] 
    booked = Available_Day.objects.filter(time_list__exact = time)[0] 
    totalSlotTime, totalSlotTime2 = getTotalSlot_Time(request) 
    date = request.session['date']
    time_list = request.session['time_list']
    if totalSlotTime2 != 0:
        numberdec = (totalSlotTime2 / 0.5) - 1
    else: 
        numberdec = 0
    remove_slot = time + totalSlotTime + numberdec
    for v in range(time, remove_slot + 1):
        time_list.remove(v)
        print(v)
    return JsonResponse('payment Completed', safe = False)

    
import socket
socket.gethostbyname("www.google.com")  
def payment_successful(request):
    TIMESLOT_LIST = (
        (0, '09:00'),
        (1, '09:30'),
        (2, '10:00'),
        (3, '10:30'),
        (4, '11:00'),
        (5, '11:30'),
        (6, '12:00'),
        (7, '12:30'),
        (8, '13:00'),
        (9, '13:30'),
        (10,'14:00'),
        (11, '14:30'),
        (12, '15:00'),
        (13, '15:30'),
        (14, '16:00'),
        (15, '16:30'),
        (16, '17:00'),
        (17, '17:30'),
        (18, '18:00')
    )
    d = dict(TIMESLOT_LIST)
    time = request.session['time']
    time = d[time]
    date = request.session['date']
    items, totalPrice, totaltime = getBasketFormatted(request)
    args =  {'name': request.session['name'], 'ID': request.session['transaction_id'], 'time': time, 'date': date, 'items': items, 'totalPrice': totalPrice, 'totaltime': totaltime}
    template = render_to_string('email_template.html', args)
    send_mail( 
                         'Booking successful confirmation!',
                         template,
                         settings.EMAIL_HOST_USER, 
                         [request.session['email']],
                         fail_silently= False
                         )
    request.session.flush()
    return render(request, "success.html", {})
                

