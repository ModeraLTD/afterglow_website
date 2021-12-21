from django.db import models

# Create your models here.
class Product(models.Model):
    """Model representing a single product"""

    name = models.CharField(max_length=16)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField()

    def __str__(self):
        return self.name