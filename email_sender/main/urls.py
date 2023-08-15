"""url patterns"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='home'), #main page
    url(r'^register', views.registration_view, name='register'),#register user
    url(r'^login', views.login_view, name='login'),#log in user
    url(r'^logout', views.logout_view, name='logout'),#log out
    url(r'^sub_list', views.list_of_subscribers, name='sub_list'), #list of subscribers page 
    url(r'^add_sub', views.add_sub_view, name='add_sub'), #add new subscriber
    url(r'^del_sub', views.del_sub_view, name='del_sub'), #delete subscriber
    url(r'^newsletter', views.newsletter_view, name='newsletter'), #newsletter page
    url(r'^new_newsletter', views.create_newsletter_view, name='create_newsletter'), #send new mail list
    url(r'^sent_emails', views.sent_emails_view, name='sent_emails'), # sent emails page
    url(r'^show_message', views.show_message_view, name='show_message'), #get body of message
    url(r'^img/(?P<track_number>\w+)/$', views.track_detail, name='track_detail'), #record the opening of an email

]