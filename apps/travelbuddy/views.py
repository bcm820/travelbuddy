from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import bcrypt



### Login & Registration ###

# /
def index(request):
    return render(request, 'travelbuddy/index.html')

# /register/
def register(request):
    if request.method == 'GET': # Block GET requests
        return redirect('/')
    
    # Validate registration form and show errors
    errors = User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            messages.error(request, message, extra_tags=field)
        return redirect('/')

    else: # If inputs valid, create new user
        User.objects.create(
            name = request.POST["name"],
            username = request.POST["username"],

            # Encrypt user password and store in DB
            password = bcrypt.hashpw(
                request.POST["password"].encode(), bcrypt.gensalt()
            )
        )

        # Store session for login and queries
        request.session['user'] = request.POST["username"]
        return redirect('/travels/')

# /login/
def login(request):
    if request.method == 'GET':
        return redirect('/')

    # Validate registration form and show errors
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            messages.error(request, message, extra_tags=field)
        return redirect('/')

    else: # If inputs valid, store session for login and queries
        request.session['user'] = request.POST["username"]
        return redirect('/travels/')

# /logout/
def logout(request):
    if 'user' in request.session:
        request.session.flush() # Deletes session data and cookie
        messages.error(request, "You have closed your session. Thank you!")
    return redirect('/')



### Main Site ###

# /travels/
def main(request):
    if not 'user' in request.session: # Redirect logged out user
        messages.error(request, "You must login to view our site.")
        return redirect('/')

    user = User.objects.get(username=request.session['user'])
    
    data = {
        # get user info
        "user": user,
        
        # get trip lists: one for user, another for user to join trips
        "user_trips": Trip.objects.filter(users=user),
        "other_trips": Trip.objects.exclude(users=user)
    }
    return render(request, 'travelbuddy/main.html', data)

# /travels/add/
def add(request):
    if not 'user' in request.session:
        messages.error(request, "You must login to view our site.")
        return redirect('/')
    return render(request, 'travelbuddy/add.html')

# /travels/trip/<id>/
def show(request, id):
    if not 'user' in request.session:
        messages.error(request, "You must login to view our site.")
        return redirect('/')

    data = {
        # get individual trip info
        "trip": Trip.objects.get(id=id),

        # get other users joining the trip
        "users": Trip.objects.get(id=id).users.all().order_by()
    }
    return render(request, 'travelbuddy/show.html', data)



### User Actions ###

# /travels/trip/<id>/join/
def join(request, id):
    if not 'user' in request.session: # Redirect logged out user
        messages.error(request, "You must log back in to join another trip.")
        return redirect('/')

    # Add user in session to trip
    Trip.objects.get(id=id).users.add(
        User.objects.get(username=request.session['user']))
    return redirect('/travels/')

# /travels/add/post/
def post(request):
    if request.method == 'GET':
        return redirect('/travels/add/')
    
    # validate and show errors
    errors = Trip.objects.validate(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            messages.error(request, message, extra_tags=field)
        return redirect('/travels/add/')

    else: # create new trip
        Trip.objects.create(
            destination = request.POST["destination"],
            plan = request.POST["plan"],
            start = request.POST["start"],
            end = request.POST["end"],
            host = User.objects.get(username=request.session['user'])
        )

        # Add user in session to trip as one of the 'users'
        Trip.objects.last().users.add(
            User.objects.get(username=request.session['user']))
        return redirect('/travels/')