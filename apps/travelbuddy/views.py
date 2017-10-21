from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from models import Trip
from forms import RegisterForm, LoginForm




# TO Implement:
# - Django's class-based forms (with validation)
# - Django's session approach
# - Django's authentication model
# - OAuth 2.0


### Login & Registration ###

# /
def index(request):
    # (auth) Include class RegisterForm in forms.py
    forms = {
        "registration": RegisterForm(),
        "login": LoginForm()
        }
    return render(request, 'travelbuddy/index.html', forms)

# /register/
def register(request):
    if request.method == 'GET': # Block GET requests
        return redirect('/')

    # (auth) Create new Django user
    # .create_user() default params: username, email, and password
    # for password, Django implements its own encryption
    user = User.objects.create_user(
        request.POST["username"],
        email = None,
        password = request.POST["password"] )

    # additional parameter: 'name'
    user.name = request.POST["name"]

    # Store session for login and queries
    request.session['user'] = request.POST["username"]
    return redirect('/travels/')

# /login/
def login(request):
    if request.method == 'GET':
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

    # Use username in session to query user info
    user = User.objects.get(username=request.session['user'])
    
    data = {
        # get user info
        "user": user,

        # get trip lists:
        "user_trips": user.going.all(), # where user is going
        "other_trips": Trip.objects.exclude(users=user) # not going
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

        # get all users going (via template: IF user = host, exclude!)
        "users": Trip.objects.get(id=id).users.all()
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
        # On the trip page, don't show on list via IF statement
        Trip.objects.last().users.add(
            User.objects.get(username=request.session['user']))
        return redirect('/travels/')