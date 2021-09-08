
import os

from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template import loader

from time import sleep
import json

from .models import (Customer)

from .serializers import (CustomerSerializer)

import us


class RegisterCustomerAPIView(ListCreateAPIView):
    """
    Used to register customer
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        
        # get state code
        try:
            request_data["State"] = (us.states.lookup(request_data["State"])).fips
        except:
            request_data["State"] = 111

        print(request_data["State"])

        serializer = CustomerSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()

            return Response({"status": "Success"}, status=status.HTTP_200_OK)

        else:
            print('error', serializer.errors)
            return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

class SubscriptionAPIView(ListCreateAPIView):
    """
    Used to add subscription
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def post(self, request, *args, **kwargs):
        request_data = request.data
        customer = Customer.objects.filter(EmailAddr=request_data["EmailAddr"], SEUsername=request_data["SEUsername"]).order_by('-SignUpDate')[0]
        customer.PaymentID = request_data["subscriptionID"]
        customer.save()

        # send payment success message to customer
        message_subject = "MySolarSentinel Welcomes You"
        message_content = "Payment successful. Welcome on board, thank-you very much for your business."
        html_message = loader.render_to_string(
            'payment_success.html',
            {'firstname': customer.FirstName}
        )
        send_message_to(request_data["EmailAddr"], message_subject, html_message)
        sleep(2)
        # send payment notify message to admin
        message_subject = f"New Customer: {customer.FirstName} {customer.LastName}"
        state_str = str(customer.State)
        if customer.State < 10:
            state_str = "0" + state_str

        state = us.states.lookup(state_str).abbr
        html_message = loader.render_to_string(
            'payment_notify.html',
            {'FirstName': customer.FirstName,
            'LastName': customer.LastName,
            'Addr1': customer.Addr1,
            'Addr2': customer.Addr2,
            'State': state,
            'ZipCode': customer.ZipCode,
            'EmailAddr': customer.EmailAddr,
            "CellPhone": customer.CellPhone,
            "CarrierCode": settings.CARRIER[customer.CarrierCode],
            "SEUsername": customer.SEUsername,
            "SEPassword": customer.SEPassword
            }
        )
        send_message_to("Payments@MySolarSentinel.com", message_subject, html_message)


        serializer = CustomerSerializer(data=request_data)
        # if serializer.is_valid():
        #     serializer.save()

        return Response({"status": "Success"}, status=status.HTTP_200_OK)

        # else:
        #     print('error', serializer.errors)
        #     return Response(serializer.errors,
        #                 status=status.HTTP_400_BAD_REQUEST)

def send_message(request):
    if request.method == "GET":
        content = "Test"
        reply_to_email = "payments@mysolarsentinel.com"
        subject = "Test"
    else:
        reply_to_email = json.loads(request.body.decode('utf-8'))["email"]
        subject = json.loads(request.body.decode('utf-8'))["subject"] + "-" + reply_to_email
        content = json.loads(request.body.decode('utf-8'))["content"] 

    email = EmailMessage(
        subject,
        content,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL],
        reply_to=[reply_to_email],
    )
    email.send(fail_silently=False)
    print("email sent")
    return HttpResponse("Success")

def send_message_to(email, title, content):
    send_mail(title,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=content,
        fail_silently=False
    )

