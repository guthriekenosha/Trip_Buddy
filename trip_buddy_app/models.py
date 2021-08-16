from django.db import models
import re


class UserManager(models.Manager):
     def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be 2 characters or more"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be 2 characters or more"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match"
        return errors
        # accounts_created= User.objects.filter(email = postData['email'])
        # if len(accounts_created) >= 1:
        #     errors['duplicate'] = "Email already exists."
        # if len(postData['password']) < 5:
        #     errors['password'] = "Password must be at least 5 characters"
        # if len(postData['password']) != postData['confirm_password']:
        #     errors['pw_match'] = "Password must match!"
        # return errors

class TripManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 3:
            errors['destination'] = "Destination must be 3 characters or more"
        if len(postData['plan']) < 3:
            errors['plan'] = "Plan must be 3 characters or more"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trips(models.Model):
    destination= models.CharField(max_length=75)
    plan = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

# class Edit_Trip(models.Model):
#     destination= models.CharField(max_length=75)
#     plan = models.CharField(max_length=255)
#     start_date = models.DateTimeField(auto_now_add=True)
#     end_date = models.DateTimeField(auto_now_add=True)