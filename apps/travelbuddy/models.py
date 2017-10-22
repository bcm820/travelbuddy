from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
import bcrypt
from datetime import datetime


# Form Validations

def nameMinLength(value):
    if len(value) < 3:
        raise ValidationError('"{}" is too short. Use at least 3 characters.'.format(value))

def pwMinLength(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters.')


### User & Trip models ###

class User(models.Model):
    name = models.CharField(max_length=45, validators=[nameMinLength])
    username = models.CharField(max_length=45, validators=[nameMinLength])
    password = models.CharField(max_length=100, validators=[pwMinLength])
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # When called in shell, return in string format
    def __str__(self):
        return '{} ({})'.format(self.name, self.username)

    # Returns url to access an instance of the model.
    def get_absolute_url(self):
        return reverse('view', args=[str(self.id)])

class Trip(models.Model):
    destination = models.CharField(max_length=45)
    start = models.DateTimeField()
    end = models.DateTimeField()
    plans = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Trip.objects.get(id=1).host gets the User hosting Trip1
    # User.objects.get(id=1).hosting.all() gets the trips User1 will host
    host = models.ForeignKey(User, related_name="hosting")

    # Trip.objects.get(id=1).users.all() gets the users going on Trip1
    # User.objects.get(id=1).going.all() gets the trips User1 is going on
    users = models.ManyToManyField(User, related_name="going")

    # When called in shell, return in string format
    def __str__(self):
        return '{}: {} - {} ({})'.format(
            self.destination,
            self.start.strftime('%m/%d'),
            self.end.strftime('%m/%d'),
            self.end.strftime('%Y'),
            )