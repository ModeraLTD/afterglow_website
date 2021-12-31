from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
# Create your models here.


import datetime
import uuid
import string
import random

CHARSET = list(string.ascii_uppercase + string.ascii_lowercase + string.digits)

def randomProdID():
    return "".join([random.choice(CHARSET) for i in range(8)])


class Service(models.Model):
    """Model representing a specific service (cosmetic procedure)"""
    """
    Default:
    Skin
        derma planing					40
        deluxe derma planing			75
        custom made facial				55
        chemical peel 					90
        micro needling					99
        deluxe microneedling with peel	140

    Health
        vitamin b12 injection			35
        biotin injection				50
        anti wrinkle injection			50

    Non-Invasive
        dermal fillers					50
        lips 1ml						200
        lips 2ml						325
        nasolabial folds 1ml			180
        nasolabial folds 2ml			300
        marionette lines 1ml			180
        chin 1ml						200
        chin 2ml						325
        cheeks	1ml						275
        cheeks	2ml						400
        non surgical rhinoplasty		375
        filler disolve					125

    Appearance
        profhilo face and neck (1)		350
        profhilo face and neck (2)		525
        jalupro for dark circles		200
        jalupro full face				300
        jalupro full face and neck		375
        injectable mesotherpay			175
        aqualyx thing					50
	    double chin 					300
"""

    SERVICE_CATEGORIES = {
        ("SKIN", "Skin"),
        ("HEALTH", "Health"),
        ("NON_INV", "Non-invasive procedure"),
        ("APP", "Appearance"),
    }
    prodID = models.CharField(editable=False, default=randomProdID, max_length=8)
    category = models.CharField(max_length=7, choices=SERVICE_CATEGORIES, default="SKIN")
    name = models.CharField(max_length = 40)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time = models.IntegerField(default = 30, help_text = "Time only 30 minutes and 60 minutes allowed.")# default 1h0m
    slot_time = models.DecimalField(default = 0.5, max_digits = 2, decimal_places = 1)
    description = models.TextField(default="")
    imgUrl = models.CharField(
        "URL to image",
        max_length=128,
        help_text="If the static file `css/images/<name>.png` does not exist, use this url",
        default="https://via.placeholder.com/100"
    )
    
    def __str__(self):
        return f'[{self.category}/{self.prodID}] {self.name}: £{self.price}, {self.time}'
class Customer(models.Model):
        # booking ID shown to the customer *and* client
        # used for human referenced, as a secondary key
        fullname = models.CharField("Full Name", max_length = 20, default = None)
        email = models.EmailField(max_length = 254, default = None)
        phone = models.CharField("Phone", max_length = 11, default = None)
        
        def __str__(self): 
            return f'{self.fullname}'

#Allow the admin to create days when available
class Available_Day(models.Model):
    days = models.DateField("Create Available Dates")
    
    def time_list(self):
        #List of slots availabble, instantiated each date
        time_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    
    def save(self, *args, **kwargs ):
        if self.days < datetime.date.today():
            raise ValidationError("date must be in future", code = 'invalid')
        super(Available_Day, self).save(*args, **kwargs)
    
    class Meta: 
        db_table = "Dates"
    
    def __str__(self):
        return f'{self.days}'
class Booking(models.Model):
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
        (18, '16:00')
    )
    """Model representing an appointment/booking"""
    uuid = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    date = models.ForeignKey(Available_Day, related_name = "availability", null = True, on_delete = models.SET_NULL, default = False)
    Time_From = models.IntegerField(choices = TIMESLOT_LIST)
    # randomly generated unique ID  - shouldn't be touched, modified nor used by the client/customer
    class Meta: 
        unique_together = ('date', 'Time_From')
    # randomly generated booking ID
    
    def __str__(self): 
        return f'{self.date} - {self.time}'
    
            
        
class Order(models.Model): 
    """ Order of the item """
    uuid = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, related_name = "customer", null = True, on_delete = models.SET_NULL)
    booking = models.ForeignKey(Booking, related_name = 'booking', null = True, on_delete = models.SET_NULL)
    service = models.ForeignKey(Service, related_name = 'Service', null = True, on_delete = models.SET_NULL)
    complete = models.BooleanField(default = False, null = True, blank = False)
    date_ordered = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'Date Ordered: {self.date_ordered} Customer: {self.customer} Booking Date/Time: {self.booking} Service: {self.service} Transaction: {self.complete}'
    