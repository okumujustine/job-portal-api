
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.conf import settings

from mailjet_rest import Client


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()

    def send_activation_link(user):
        token = RefreshToken.for_user(user).access_token

        absurl = settings.FRONT_END_URL + \
            "/auth/email-verify/"+user.email+"/"+str(token)

        mailjet = Client(auth=(settings.MAILJET_API_KEY,
                               settings.MAILJET_API_SECRET), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "okumujustine01@gmail.com",
                        "Name": "justine@JobsUg"
                    },
                    "To": [
                        {
                            "Email": user.email,
                            "Name": user.first_name
                        }
                    ],
                    "Subject": "JobsUg Registration!",
                    "TextPart": "Welcome to JobsUg!",
                    "HTMLPart": "<div><h3>Dear " + user.first_name + "</h3> <br/> click here to verify your email address.<h1><a href="+absurl+">Click Here</a></h1> <br/> Or you can follow the link below.<br/> "+absurl+"</div>"
                }
            ]
        }
        mailjet.send.create(data=data)

    def send_reset_password_link(user, password_reset_url):

        mailjet = Client(auth=(settings.MAILJET_API_KEY,
                               settings.MAILJET_API_SECRET), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "okumujustine01@gmail.com",
                        "Name": "justine@JobsUg"
                    },
                    "To": [
                        {
                            "Email": user.email,
                            "Name": user.first_name
                        }
                    ],
                    "Subject": "JobsUg Password Reset!",
                    "TextPart": "Thanks for using JobsUg!",
                    "HTMLPart": "<div><h3>Dear " + user.first_name + "</h3> <br/> click here to reset your password.<h1><a href="+password_reset_url+">Click Here</a></h1> <br/> Or you can follow the link below.<br/> "+password_reset_url+" < /div >"
                }
            ]
        }
        mailjet.send.create(data=data)
