from django.db import models
import re
import bcrypt
from datetime import datetime, date

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        try:
            birthdate = datetime.strptime(postData["birthday"], '%Y-%m-%d').date()
        except ValueError:
            birthdate = date.today()
        print((date.today()-birthdate).days)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters!"
        if (date.today()-birthdate).days < 4745: #365 * 13
            errors["birthday"] = "Your need to be at least 13 years old to create an account!"
        if birthdate >= date.today():
            errors["birthday"] = "Your birthday needs to be in the past!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if postData['password'] != postData['password_conf']:
            errors['password'] = "Your passwords don't match!"
        return errors
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    birthdate = models.DateField()
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
