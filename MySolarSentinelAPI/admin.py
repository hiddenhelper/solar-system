from django.contrib import admin

from .models import (Customer, SupportTickets)

admin.site.register(Customer)
admin.site.register(SupportTickets)