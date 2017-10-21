from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
    def validate_registration(self, post_data):
        errors = {}

        for field, value in post_data.iteritems():
            if field == "name":
                if len(value) < 3:
                    errors[field] = "Error: Name must be at least 3 characters."
            if field == "username":
                if len(value) < 3:
                    errors[field] = "Error: Username must be at least 3 characters."
            if field == "password":
                if len(value) < 8:
                    errors[field] = "Error: Password must be at least 8 characters."
            if field == "confirmation":
                if not value == post_data['password']:
                    errors[field] = "Error: Password entries do not match."
        return errors

    def validate_login(self, post_data):
        errors = {}

        # Only check password if username exists in DB, or there will be an exception
        for field, value in post_data.iteritems():
            if field == "username":
                if len(self.filter(username = post_data[field])) < 1:
                    errors[field] = "Error: Username not found."
                else:
                    truepass = self.get(username=post_data['username']).password
                    if not bcrypt.checkpw(post_data['password'].encode(), truepass.encode()):
                        errors[field] = "Error: Password invalid."
        return errors


class TripManager(models.Manager):
    def validate(self, post_data):
        errors = {}
        for field, value in post_data.iteritems():
            if not field == "csrfmiddlewaretoken":
                if len(value) < 1:
                    errors[field] = "Error: the {} field is required.".format(field)
                else:
                    dateformat = "%Y-%m-%d"
                    start = datetime.strptime(post_data["start"], dateformat)
                    end = datetime.strptime(post_data["end"], dateformat)
                    
                    if start < datetime.now() or end < datetime.now():
                        errors[field] = "Your travel dates must be set in the future!"
                    if end < start:
                        errors[field] = "Your trip end date must be later than your start date!"         
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return '{} ({})'.format(self.name, self.username)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    plan = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __str__(self):
        return '{}: {} - {} ({})'.format(
            self.destination,
            self.start.strftime('%m/%d'),
            self.end.strftime('%m/%d'),
            self.end.strftime('%Y'),
            )

    # Trip.objects.get(id=1).host gets the User hosting Trip1
    # User.objects.get(id=1).hosting.all() gets the trips User1 will host
    host = models.ForeignKey(User, related_name="hosting")

    # Trip.objects.get(id=1).users.all() gets the users going on Trip1
    # User.objects.get(id=1).going.all() gets the trips User1 is going on
    users = models.ManyToManyField(User, related_name="going")