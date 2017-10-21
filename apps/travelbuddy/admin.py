from __future__ import unicode_literals
from django.contrib import admin

# Import models
from models import User, Trip

# Create admin classes
class UserAdmin(admin.ModelAdmin):
    pass

class TripAdmin(admin.ModelAdmin):
    pass

# Create instances of admins
admin.site.register(User, UserAdmin)
admin.site.register(Trip, TripAdmin)