from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics, views, status
from rest_framework.response import Response

from .serializers import ContactUsSerializer
from .models import Contact
# Create your views here.


class ContactUsCreateView(generics.GenericAPIView):
    serializer_class = ContactUsSerializer

    def post(self, request):
        contactus = request.data
        serializer = self.serializer_class(data=contactus)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        contactus_data = serializer.data

        return Response(contactus_data, status=status.HTTP_201_CREATED)
