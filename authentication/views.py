from django.shortcuts import render
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from drf_yasg import openapi
import jwt
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os

from .serializers import (RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ReVerifyEmailSerializer,
                          ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, UserSerializer, LogoutSerializer, UserProfileSerializer, UserProfileUpdateSerializer)
from .models import CustomUser, Profile
from .utils import Util
from .renderers import UserRenderer

# Create your views here.


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME', ''), 'http', 'https']


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)

        user_already_exists = CustomUser.objects.filter(email=user['email'])

        if user_already_exists.exists():
            return Response({"error": "User with provided email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = CustomUser.objects.get(email=user_data['email'])

        Util.send_activation_link(user)
        # // send activation link disabled

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    email_param_config = openapi.Parameter(
        'email', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    # @swagger_auto_schema(manual_parameters=[token_param_config, email_param_config]) #swagger

    def get(self, request):
        token = request.GET.get('token')
        email = request.GET.get('email')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = CustomUser.objects.get(id=payload['user_id'])

            if not user:
                return Response({"error": "User does not exists"}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_verified:
                user.is_verified = True
                user.save()
                return Response({"email": "Successfuly activated"}, status=status.HTTP_200_OK)

            return Response({"email": "Already activated"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignature as identifier:
            # send a new link
            user = CustomUser.objects.get(email=email)

            if not user:
                return Response({"error": "User does not exists"}, status=status.HTTP_400_BAD_REQUEST)

            Util.send_activation_link(user, request)

            return Response({"error": "Expired activation link, a new link has been sent to your email account", "status": "newlink"}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        if not request.data['email']:
            return Response({"error": "Provide email or password and try again"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data['password']:
            return Response({"error": "Provide email or password and try again"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReVerifyEmail(generics.GenericAPIView):
    serializer_class = ReVerifyEmailSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.get(email=serializer.data['email'])

        Util.send_activation_link(user, request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):

        email = request.data['email']

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            password_reset_url = settings.FRONT_END_URL + \
                "/auth/confirm-password-reset/"+str(uidb64)+"/"+str(token)

            Util.send_reset_password_link(user, password_reset_url)

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        return Response({'error': 'Email address not registered'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(f'{redirect_url}?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    f'{redirect_url}?token_valid=True&?message=Credentials Valid&?uidb64={uidb64}&?token={token}'
                )

            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return CustomRedirect(f'{redirect_url}?token_valid=False')


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LoggedInUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        profile = Profile(owner=self.request.user)
        return self.request.user


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserProfileView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    # def perform_update(self, serializer)


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = "owner"
    permission_classes = (IsAuthenticated,)
