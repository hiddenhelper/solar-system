from django.urls import path
from django.conf.urls import include, url

from MySolarSentinelAPI.views import (RegisterCustomerAPIView)
from MySolarSentinelAPI.views import (SubscriptionAPIView)
from MySolarSentinelAPI import views

urlpatterns = [
    path(
        'register_customer/',
        RegisterCustomerAPIView.as_view(),
        name = "RegisterCustomer"
    ),
    path(
        'paypal_subscription_complete/',
        SubscriptionAPIView.as_view(),
        name = "Subscription"
    ),
    # path(
    #     'send_message/',
    #     MessageHandleAPIView.as_view(),
    #     name = "MessageHandle"
    # ),
    url(r"^send_message/$", views.send_message, name="send_message")
]