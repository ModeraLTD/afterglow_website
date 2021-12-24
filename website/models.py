from django.db import models

# Create your models here.
from django.conf import settings

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
    length = models.TimeField("Length of service (minutes)", default=datetime.time(1, 0))  # default 1h0m
    description = models.TextField(default="")
    imgUrl = models.CharField(
        "URL to image",
        max_length=128,
        help_text="If the static file `css/images/<name>.png` does not exist, use this url",
        default="https://via.placeholder.com/100"
    )
    
    def __str__(self):
        return f'[{self.category}/{self.prodID}] {self.name}: £{self.price}'


class Booking(models.Model):
    """Model representing an appointment/booking"""
    # randomly generated unique ID  - shouldn't be touched, modified nor used by the client/customer
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # randomly generated booking ID
    
    # booking ID shown to the customer *and* client
    # used for human referenced, as a secondary key
    booking_id = models.CharField("Booking ID for user", max_length=8, default=None)
    
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    time_from = models.DateTimeField("Starting date/time of booking", default=datetime.datetime(2021, 1, 1, 0, 0, 0))
    time_to = models.DateTimeField("Ending date/time of booking", default=datetime.datetime(2021, 1, 1, 0, 0, 0))
    firstName = models.CharField("First name of booker", max_length=16, default=None)
    lastName = models.CharField("Last name of booker", max_length=32, default=None)
    address = models.CharField("Address of booker", max_length=256, default=None)

    def __str__(self): 
        return f'<{self.uuid}> [{self.time_from.strftime("%D %T")} - {self.time_to.strftime("%T")}] {Service.category} by {self.firstName} {self.lastName} at {self.address}'

