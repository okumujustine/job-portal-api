
from django.urls import path
from .views import (ContactUsCreateView)

app_name = "contactus"


urlpatterns = [
    path('create/', ContactUsCreateView.as_view(), name='contactus-create'),
]
