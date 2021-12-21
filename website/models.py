from django.db import models

# Create your models here.
from django.conf import settings

import datetime
import uuid

class Service(models.Model):
    """Model representing a specific service (cosmetic procedure)"""
    SERVICE_CATEGORIES = {
        ("SKIN", "Skin"),
        ("HEALTH", "Health"),
        ("NON_INV", "Non-invasive procedure"),
        ("APP", "Appearance"),
    }

    category = models.CharField(max_length=7, choices=SERVICE_CATEGORIES, default="SKIN")
    name = models.CharField(max_length = 20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f'[{self.category}] {self.name}: £{self.price}'

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