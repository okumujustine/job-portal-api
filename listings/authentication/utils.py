
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.conf import settings


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()
        # return Response({"error": "Failed to send verification email, try again later"}, status=status.HTTP_400_BAD_REQUEST)

    def send_activation_link(user, request):
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        # absurl = 'http://'+current_site+relativeLink+"?email="+user.email+"&token="+str(token)
        absurl = settings.FRONT_END_URL+"/"+user.email+"/"+str(token)

        email_body = 'Hi ' + user.first_name + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
