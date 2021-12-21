from django.db import models

# Create your models here.
from django.conf import settings

# Create your models here.

class service(models.Model):
    SERVICE_CATEGORIES = {
        ('Face', "Full Face"),
        ('Body', "Full body"),
        ('Pack', "Full packages")
    }
    
    number = models.IntegerField()
    category = models.CharField(max_length =4, choices = SERVICE_CATEGORIES)
    name = models.CharField(max_length = 20)
    price = models.IntegerField()
    
    def __str__(self):
        return f'from {self.category} created {self.number} {self.name} for £{self.price}'
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    Service = models.ForeignKey(service, on_delete = models.CASCADE)
    bookin = models.DateTimeField()
    bookout = models.DateTimeField
    
    def __str__(self):
        return f'{self.user} has booked {self.Service} from {self.bookin} to {self.bookout}'