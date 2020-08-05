from django.db import models
from login.models import *

# Create your models here.
class ProductManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Quaranthing name must be at least 2 characters!"
        if len(postData['description']) < 10:
            errors['description'] = "Use at least 10 characters to describe your Quaranthing!"
        if postData['stock'] < 1:
            errors['stock'] = "At least one of this Quaranthing must be available for it to be listed!"
        # if postData['price'].
        try:
            # price = round(postData['price'], 2)
            if postData['price'] >= 10000 or postData['price'] < 0:
                errors['price'] = "Your Quaranthing price is not between $0 and  $9999.99!"
        except TypeError:
            errors['price'] = "Your Quaranthing price is not a number!"
        return errors
class Product(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) #allow for items to be priced no more than $9999.99
    stock = models.IntegerField() #how many of this product is in stock
    seller = models.ForeignKey(User, related_name = "products_listed", on_delete = models.CASCADE)
    objects = ProductManager()
