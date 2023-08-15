from __future__ import unicode_literals

from .forms import RegistrationForm, LoginForm, NewSubscriberForm,RecipientForm
from .services import UserManagement, SubManagement
from .models import SentMessage, Subscriber
from .task import send_delayed_email,send_email_task
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from django.template import Template, Context
from datetime import timedelta, datetime

def main_page(request):
    """open main page"""    
    reg_form = RegistrationForm()
    login_form = LoginForm()
    context = {'reg_form':reg_form,'login_form':login_form}
    return render(request,'main_page.html',context)

def registration_view(request):
    """create new user """
    if request.method == 'POST':
        if UserManagement.register_user(request):
            return redirect('home')
        else:
            return redirect('home')

    else:
        return render(request,'main_page.html')
    

def login_view(request):
    """log in user"""
    if request.method == 'POST':
        if UserManagement.login_user(request):
            return redirect ('home')
        else:
            return redirect ('home')
    else:
        return redirect('home')

def logout_view(request):
    """log out user """
    UserManagement.logout_user(request)
    return redirect('home')

@login_required
def list_of_subscribers(request):
    """open list of subscribers page"""
    add_sub_form = NewSubscriberForm(initial={'user': request.user})
    context = {'sub_list':SubManagement.list_of_subscribers(request),
                'add_sub_form':add_sub_form}
    return  render(request,'list_of_subscribers.html',context)

@login_required
def add_sub_view(request):
    """adding new subscriber"""
    if SubManagement.add_sub(request):
        return JsonResponse({'email': request.POST.get('email')})
    else:
        return JsonResponse({'message': 'Error'})

@login_required
def del_sub_view(request):
    """delete subscriber"""
    if SubManagement.del_sub(request):
        return JsonResponse({'message': 'Complete'})
    else:
        return JsonResponse({'message': 'Error'})

@login_required
def newsletter_view(request):
    """page of mail sending"""
    form = RecipientForm(user=request.user) 
    context = {
        'sub_list': SubManagement.list_of_subscribers(request),
        'form': form
    }
    return render(request, 'newsletters.html', context)

@login_required
def create_newsletter_view(request):
    """new mail sending"""
    if request.method == "POST" and request.is_ajax():
        email_data={}
        form = RecipientForm(request.POST)
        
        if form.is_valid():
            recipients=form.cleaned_data['recipients']
            list_of_recipients = []
            delayed_start = request.POST.get('delayed_start')
            email_data['sender_id'] = request.user.id
            email_data['subject'] = request.POST.get('subject')
            email_data['sender_email'] = request.POST.get('sender_email')
            email_data['sender_password'] = request.POST.get('password')
            email_data['message_template'] = request.POST.get("lettertext")
            for recipient in recipients: #record recipients data
                recipient_data={}
                recipient_data['id']=recipient.id
                recipient_data['first_name']=recipient.first_name
                recipient_data['last_name']=recipient.last_name
                recipient_data['email']=recipient.email
                recipient_data['date_of_birth']=recipient.date_of_birth
                list_of_recipients.append(recipient_data)
            email_data['list_of_recipients'] = list_of_recipients
            
            if delayed_start: 
                send_delayed_email.apply_async(args=[email_data],eta = delayed_start)
            else:
                send_email_task.delay(email_data)
        
            return JsonResponse({"message": "Complete!"})
        else:
            return JsonResponse({"message": "Error."}, status=400)
@login_required
def sent_emails_view(request):
    """list of sent message and their status"""
    sent_messages = SentMessage.objects.filter(user=request.user)
    context = {'messages':sent_messages}
    return render(request,'sent_emails.html',context)


@login_required
def show_message_view(request):
    """get message text"""
    message_id = request.POST.get('message_id')
    message = SentMessage.objects.get(id = message_id)
    print(message.message)
    return JsonResponse({'text':message.message})

def track_detail(request,track_number):
    """registration the opening of an email"""
    message = SentMessage.objects.get(track_num=track_number)
    message.status = 'viewed'
    message.save()
    image_path = '/home/seksualka/email/email_sender/static/1x1_#4B61BFFF.png'
    with open(image_path, 'rb') as img_file:
        response = HttpResponse(img_file.read(), content_type='image/jpeg')
        return response
    
