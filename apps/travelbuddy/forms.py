from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=45)
    username = forms.CharField(max_length=45)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(max_length=100,widget=forms.PasswordInput)
    # UserManager()?

class LoginForm(forms.Form):
    username = forms.CharField(max_length=45)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    # UserManager()?

class TripForm(forms.Form):
    destination = forms.CharField(max_length=45)
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)
    plans = forms.CharField(max_length=100)
    # TripManager()?