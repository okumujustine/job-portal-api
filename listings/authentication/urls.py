
from django.urls import path
from .views import (RegisterView, VerifyEmail, LoginAPIView, ReVerifyEmail, RequestPasswordResetEmail,
                    PasswordTokenCheckAPI, SetNewPasswordAPIView, LoggedInUser, LogoutAPIView)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('re-verify/', ReVerifyEmail.as_view(), name="re-verify"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('user/', LoggedInUser.as_view(), name="logged-in-user"),
    path('refresh/token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/token/', TokenVerifyView.as_view(), name='token_verify'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]
