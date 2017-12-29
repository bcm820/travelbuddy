from __future__ import unicode_literals
from django.contrib import admin

# Import models
from models import User, Trip

# Create admin classes
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'username'
    )

class TripAdmin(admin.ModelAdmin):
    list_display = (
        'destination',
        'start',
        'end',
        'plans'
    )

# Create instances of admins
admin.site.register(User, UserAdmin)
admin.site.register(Trip, TripAdmin)