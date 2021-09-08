# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.db import models, connection
from django.utils import timezone
from django.core.exceptions import ValidationError
import us
import re

# get phone number
def get_phone_number(text):
    # numbers = re.finditer(r"\b[1-9]?[-. ]?\(?[2-9][0-9]{2}\)?[-. ]?[2-9][0-9]{2}[-. ]?[0-9]{4}\b", text)
    numbers = re.finditer(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", text)
    for match_number in numbers:
        return match_number.group().replace(" ", "").replace(".", "").replace("-", "").replace("(", "").replace(")", "")
    return False

# get email
def get_email(text):
    text = text.lower()
    EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    for re_match in re.finditer(EMAIL_REGEX, text):
        return re_match.group()


# State Validation
def validate_State(value):
    if value == 111:
        raise ValidationError("Please input valid State Code.")

# Email Validation
def validate_EmailAddr(value):
    email = get_email(value)
    if email != value:
        raise ValidationError("Please input valid Email.")

# CellPhone Validation
def validate_CellPhone(value):
    
    phone = get_phone_number(value)
    if phone is False:
        raise ValidationError("Please input valid Phone Number.")

    # if len(value) > 10:
    #     raise ValidationError("Please input only Numbers")

# ZipCode Validation
def validate_ZipCode(value):
    if len(str(value)) != 5:
        raise ValidationError("Please input valid zip code")

# validate_CarrierCode Validation
def validate_CarrierCode(value):
    print("======", value)
    if value == -1:
         raise ValidationError("Please select Carrier Code.")
        
class Customer(models.Model):
    SignUpDate = models.DateTimeField('date joined', default=timezone.now)
    PaymentID = models.CharField(max_length=15, null=True, blank=True)
    SiteID = models.CharField(max_length=10, null=True, blank=True)
    FirstName = models.CharField(max_length=20, null=True, blank=False)
    LastName = models.CharField(max_length=20, null=True, blank=False)
    Addr1 = models.CharField(max_length=30, null=True, blank=False)
    Addr2 = models.CharField(max_length=30, null=True, blank=False)
    State = models.IntegerField(null=True, blank=False, validators=[validate_State])
    ZipCode = models.IntegerField(null=True, blank=False, validators=[validate_ZipCode])
    CellPhone = models.CharField(max_length=17, null=False, blank=False, validators=[validate_CellPhone])
    EmailAddr = models.CharField(max_length=35, null=False, blank=False, validators=[validate_State])
    CarrierCode = models.IntegerField(null=False, blank=False, validators=[validate_CarrierCode])
    APIKey = models.CharField(max_length=40, null=True, blank=True)
    SEUsername = models.CharField(max_length=35, null=False, blank=False)
    SEPassword = models.CharField(max_length=35, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.CellPhone = get_phone_number(self.CellPhone)
        super(Customer, self).save(*args, **kwargs)

class SupportTickets(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, verbose_name='customer', on_delete=models.SET_NULL)
    TicketOpenDate = models.DateTimeField('ticket created date', default=timezone.now)
    TicketStatus = models.CharField(max_length=10, default="Create")
    CustomerAcknowledged = models.BooleanField('CustomerAcknowledged', default=False)
    TechnicianName = models.CharField(max_length=10, blank=True, null=True)
    Notes = models.CharField(max_length=1024, blank=True, null=True)
