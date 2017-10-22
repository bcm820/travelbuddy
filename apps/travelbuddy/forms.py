from django import forms
from django.core.exceptions import ValidationError
from models import User, Trip


# Need to fix validations

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirmation")

        if password != confirm:
            raise ValidationError("Your password entries do not match!")


# Need to fix validations

class LoginForm(forms.Form):
    username = forms.CharField(max_length=45)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)



# Need to validate for time

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['destination','start','end','plans']
        exclude = ['added', 'updated','host','users']