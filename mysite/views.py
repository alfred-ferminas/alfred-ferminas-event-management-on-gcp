from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from polls.models import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

def index(request):
    print(request.user.username)
    return render(request , "user/index.html")

def events(request):
    data = registeredevents.objects.all()
    context = {
        'data' : data
    }
    if request.method == "POST":
        evid = int(request.POST.get('eveid'))
        registrar = request.user
        try:
            event_instance = registeredevents.objects.get(eventid=evid)
            registered = event_instance.username
            registration_instance = registration(eventid=event_instance, username=registrar)
            registration_instance.save()
            notification(description = f"A new user {registrar} registered in your event {event_instance.eventname}.",username=registered).save()
            notification(description = f"You Sucessfully  Registered in {event_instance.eventname} event.",username=registrar).save()
            print(event_instance,registrar)
        except registeredevents.DoesNotExist:
            registration_instance = None
     
    if request.method == "GET":
        date = request.GET.get("date")
        location = request.GET.get("location")
        if date:
            data = registeredevents.objects.filter(date__icontains = date)
            context = {
                'data' : data
            }
        elif location:
            data = registeredevents.objects.filter(location__icontains = location)
            context = {
                'data' : data
            }

    return render(request , "user/allevents.html",context)
    
def notifications(request):
    data = notification.objects.filter(username=request.user.username).order_by('-id')
    formatted_datetimes = [entry.datetime.strftime('%Y-%m-%d %I:%M:%S %p') for entry in data]

    descriptions = [entry.description for entry in data]
    dates = formatted_datetimes

    zipped_data = zip(descriptions, dates)

    context = {
        'zipped_data': zipped_data
    }

    return render(request, "user/notification.html", context)
     
def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            print("login Sucessfully")
            return redirect("home")
        else:
            print("incorrect Cridentials")

    return render(request , "user/login.html")
    
def signup(request):
    if request.method == "POST":
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        if password == confirmpassword:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
            notification(description = f"Welcome {firstname}!",username=username).save()
            return render(request,"user/index.html")
        else:
            return HttpResponse("<h1>Password is not same</h1>")

    return render(request , "user/signup.html")
    
def thanks(request):
    return render(request , "user/thanks.html")
    
def contactus(request):
    if request.method == "POST":
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        usermails(email = email, subject = subject, message = message).save()
        if request.user.is_authenticated:
            notification(description = "We have received your message.We will get back soon.",username=username).save()
        return render(request,"user/thanks.html")
    return render(request , "user/contact.html")
    
def myevents(request):
    data = registeredevents.objects.filter(username = request.user.username)
    event_data = []
    for event in data:
        registrations_count = registration.objects.filter(eventid=event).count()
        event_data.append({
            'event': event,
            'registrations_count': registrations_count,
        })

    context = {
        'combined_data': zip(data, event_data),
    }
    if request.method == "POST":
        eventname = request.POST['eventname']  
        purpose = request.POST['purpose'] 
        location = request.POST['location'] 
        date = request.POST['date'] 
        typeofevent = request.POST['typeofevent'] 
        username = request.user.username
        # document = request.POST['document'] 
        registeredevents(eventname = eventname, purpose = purpose,location = location, date = date, type = typeofevent,username = username).save()

        notification(description = "Your Event is Registered",username=username).save()
        return render(request,"user/thanks.html")

    return render(request,"user/myevents.html",context)

def signout(request):
    auth_logout(request)
    print("Logout Sucessfully")
    return redirect("home")

def deleteevent(request,myid):
    event = registeredevents.objects.get(eventid=myid)
    notification(description = f"Your event {event.eventname} is Deleted.",username = request.user.username).save()
    event.delete()
    return redirect("myevents")

def notify(request,myid):
    
    data = registration.objects.filter(eventid = myid)
    if data.count() > 0:
        today = timezone.now().date()
        eventdate = registeredevents.objects.get(eventid = myid)
        remaining_days = (eventdate.date - today).days
        if remaining_days > 0:
            for i in data:
                notification(description = f"You have {remaining_days} days Left in {eventdate.eventname} Event. Be Ready!",username=i.username).save()
    else:
        notification(description = f"Reminder Error! You have no Registered Members",username=request.user.username).save()

    return redirect("myevents")

def saverecord(request,myid):
    if request.method == "POST":
        getevent = registeredevents.objects.get(eventid = myid)
        getevent.eventname = request.POST['eventname']
        getevent.purpose = request.POST['purpose']
        getevent.location = request.POST['location']
        getevent.date = request.POST['date']
        getevent.type = request.POST['typeofevent']
        getevent.save()
        notification(description = f"The information of {getevent.eventname} updated Sucessfully.",username=request.user.username).save()
    return redirect("myevents")