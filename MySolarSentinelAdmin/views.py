import os
import logging
import re
from django.shortcuts import render, redirect
from django.template import RequestContext
from datetime import datetime, date
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.template import loader
from django.db import models

from django.utils import timezone
import datetime
from datetime import timezone
import pytz
import us

from MySolarSentinelAPI.models import (Customer, SupportTickets)





######### dashbord ##########

def login(request):
    if request.user.is_authenticated: # to avoid go to login screen again without logout.
        return redirect('dashboard')

    strMessage = ""
    if request.method=='POST':
        username = request.POST['email']
        password = request.POST['password']
        if __login(request, username, password):
            return redirect('dashboard')
        else:
            strMessage = "Username or password is invalid!"
    response = render(request, "signin.html",{ "message": strMessage} )
    return response

def __login(request, username, password):
    ret = False
    user = authenticate(username=username, password=password)
    if user:
        # if user.is_active and user.is_superuser:
        if user.is_active:
            auth_login(request, user)
            ret = True
    return ret

# sign out
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # check this user is admin
    if is_admin(request) is False:
        return redirect("logout")

    user = request.user
    username = user.username

    customers = Customer.objects.all().order_by("-SignUpDate")
    for customer in customers:
        supportTicket, created = SupportTickets.objects.get_or_create(customer=customer)
        customer.TicketStatus = supportTicket.TicketStatus
        customer.SignUpDate = get_mountaintime(customer.SignUpDate)

    searched_customers = []
    
    if request.method=='POST':
        search_query = request.POST["search_input"].lower()
        for customer in customers:
            customer_string = str(list(Customer.objects.filter(id=customer.id).values())).lower()
            if search_query in customer_string:
                searched_customers.append(customer)
    
        return render(request, "dashboard.html", {"customers": searched_customers})
    
    customers = customers[:20]
    

    return render(request, "dashboard.html", {"customers": customers})

def is_admin(request):
    user = request.user
    # user = authenticate(username=username, password=password)
    if user:
        if user.is_active and user.is_superuser:
            return True
    return False

@login_required
def view_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)

    if request.method == "POST":
        print(request.POST["CarrierCode"], "======")
        customer.PaymentID = request.POST["PaymentID"]
        customer.SiteID = request.POST["SiteID"]
        customer.CellPhone = request.POST["CellPhone"]
        customer.EmailAddr = request.POST["EmailAddr"]
        if request.POST["CarrierCode"]:
            customer.CarrierCode = request.POST["CarrierCode"]
        customer.APIKey = request.POST["APIKey"]
        customer.SEUsername = request.POST["SEUsername"]
        customer.SEPassword = request.POST["SEPassword"]
        customer.save()

        return redirect("dashboard")

    else:
        customer.SignUpDate = get_mountaintime(customer.SignUpDate)
        state = us.states.lookup(str(customer.State))
        customer.State = state.abbr
        supportTicket = SupportTickets.objects.get_or_create(customer=customer)
        carrier_code = settings.CARRIER[customer.CarrierCode]

    return render(request, "view_customer.html", {"customer": customer, 
                    "carrier_code": carrier_code, "supportTicket": supportTicket})

@login_required
def view_supportTicket(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.SignUpDate = get_mountaintime(customer.SignUpDate)
    supportTicket = SupportTickets.objects.get(customer=customer)
    supportTicket.TicketOpenDate = get_mountaintime(supportTicket.TicketOpenDate)

    return render(request, "view_ticket.html", {"customer": customer, 
                 "supportTicket": supportTicket, "notes": supportTicket.Notes})

@login_required
def create_ticket(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    supportTicket = SupportTickets.objects.get(customer=customer)
    technician_name = request.POST["technician_name"]
    notes = request.POST["notes"]
    supportTicket.TicketStatus = "Open"
    supportTicket.TechnicianName = technician_name
    supportTicket.Notes = notes
    supportTicket.TicketOpenDate = datetime.datetime.now(timezone.utc)
    supportTicket.save()
    return redirect('supportTicket', customer_id)

@login_required
def edit_ticket(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    supportTicket = SupportTickets.objects.get(customer=customer)
    technician_name = request.POST["technician_name"]
    notes = request.POST["notes"]
    supportTicket.TicketStatus = "Open"
    supportTicket.TechnicianName = technician_name
    supportTicket.Notes = notes
    supportTicket.TicketOpenDate = datetime.datetime.now(timezone.utc)
    supportTicket.save()
    return redirect('supportTicket', customer_id)

@login_required
def close_ticket(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    supportTicket = SupportTickets.objects.get(customer=customer)
    supportTicket.TicketStatus = "Create"
    supportTicket.save()
    return redirect('support_tickets')

@login_required
def support_tickets(request):
    user = request.user
    username = user.username
    supportTickets = SupportTickets.objects.filter(TicketStatus="Open").order_by("-TicketOpenDate")
    for supportTicket in supportTickets:
        supportTicket.TicketOpenDate = get_mountaintime(supportTicket.TicketOpenDate)
        supportTicket.customer.SignUpDate = get_mountaintime(supportTicket.customer.SignUpDate)

    searched_tickets = []
    
    if request.method=='POST':
        search_query = request.POST["search_input"].lower()
        for ticket in supportTickets:
            ticket_string = str(list(SupportTickets.objects.filter(id=ticket.id).values())) + str(list(Customer.objects.filter(id=ticket.customer.id).values())).lower()
            if search_query in ticket_string:
                searched_tickets.append(ticket)
    
        return render(request, "support_tickets.html", {"supportTickets": searched_tickets})
    
    supportTickets = supportTickets[:20]
    
    return render(request, "support_tickets.html", {"supportTickets": supportTickets})

def get_mountaintime(utc_time):
    fmt = "%m-%d-%Y %H:%M"
    mountain_timezone = pytz.timezone('US/Pacific')
    # mountain_time = customer.SignUpDate.replace(tzinfo=mountain_timezone)
    return utc_time.astimezone(mountain_timezone).strftime(fmt)