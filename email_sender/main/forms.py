from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subscriber

class RegistrationForm(UserCreationForm):
    """form for register new user"""
    def __init__(self, *args, **kwargs):

        super(RegistrationForm,self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    """form for log in"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class NewSubscriberForm(forms.ModelForm):
    """form for adding new subscriber"""
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())
    class Meta:
        model = Subscriber
        fields = ['first_name','last_name','email','date_of_birth','user']


class RecipientForm(forms.Form):
    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(RecipientForm, self).__init__(*args, **kwargs)
            if user:
                self.fields['recipients'].queryset = Subscriber.objects.filter(user=user)

    recipients = forms.ModelMultipleChoiceField(
        queryset=Subscriber.objects.none(),  
        widget=forms.CheckboxSelectMultiple,
        required=False 
    )
    # recipients = forms.ModelMultipleChoiceField(
    #     # queryset=Subscriber.objects.all(),
    #     queryset=Subscriber.objects.none(),
    #     widget=forms.CheckboxSelectMultiple,
    #     initial=Subscriber.objects.all(),
        
    # )
    
    # excluded_recipients = forms.ModelMultipleChoiceField(
    #     queryset=Subscriber.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )