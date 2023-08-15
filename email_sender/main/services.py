"""buiseness logic"""
from .forms import RegistrationForm, LoginForm, NewSubscriberForm
from .models import Subscriber, SentMessage
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404

class UserManagement:
    """class for user management"""
    @staticmethod
    def register_user(request): 
        """new user creation"""
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            user_messages = SentMessage.objects.create(user = user, message='your text message here',
                                                        status='click here') #example of sent message 
            user_messages.save()
            return True
        else:
            return False

    @staticmethod
    def login_user(request):
        """log in user func"""
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user) 
                    return True
                else:
                    return False
            else:
                return False

    @staticmethod
    def logout_user(request):
        logout(request)

class SubManagement:
    """class for management of user subscribers"""
    @staticmethod
    def list_of_subscribers(request):
        """get list of user subscribers"""
        return Subscriber.objects.filter(user = request.user)
    
    @staticmethod
    def add_sub(request):
        """create new subscriber"""
        form = NewSubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return True
        else:
            for err in form.errors:
                print(err)
            return False
    @staticmethod
    def del_sub(request):
        """delete subscriber func"""
        sub = get_object_or_404(Subscriber, id = request.POST.get('subscriber_id'))
        sub.delete()