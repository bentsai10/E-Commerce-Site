from django.db import models
from login.models import *

# Create your models here.
class ProductManager(models.Manager):
    def validator(self, postData, fileData):
        print(fileData)
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Quaranthing name must be at least 2 characters!"
        if len(postData['description']) < 10:
            errors['description'] = "Use at least 10 characters to describe your Quaranthing!"
        if int(float(postData['stock'])) < 1:
            errors['stock'] = "At least one of this Quaranthing must be available for it to be listed!"
        if float(postData['price']) >= 10000 or float(postData['price']) < 0:
            errors['price'] = "Your Quaranthing price is not between $0 and  $9999.99!"
        if len(fileData.getlist('image')) < 1:
            errors['image'] = "Please upload at least one photo for your listing!"
        return errors
class Product(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) #allow for items to be priced no more than $9999.99
    stock = models.IntegerField() #how many of this product is in stock
    views = models.IntegerField()
    seller = models.ForeignKey(User, related_name = "products_listed", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()

class Category(models.Model):
    name = models.CharField(max_length = 255)
    category_type = models.CharField(max_length = 40)
    products = models.ManyToManyField(Product, related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
    img_file = models.ImageField(upload_to='images/') 
    caption = models.TextField(blank=True)
    products = models.ManyToManyField(Product, related_name="images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    rating = models.IntegerField()
    content = models.TextField()
    user = models.ForeignKey(User, related_name = "reviews", on_delete = models.CASCADE)
    product = models.ForeignKey(Product, related_name = "reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)