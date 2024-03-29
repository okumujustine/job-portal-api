from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save


class MainModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **other_fields):
        # other_fields.setdefault('is_verified', True)
        if not email:
            return Response({"error": "You must provide an email address"}, status=status.HTTP_400_BAD_REQUEST)

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_verified', True)
        other_fields.setdefault('role', 'admin')

        if other_fields.get('is_staff') is not True:
            # raise ValueError(_('is_staff must be true'))
            return Response({"error": "is_staff must be true"}, status=status.HTTP_400_BAD_REQUEST)

        if other_fields.get('is_superuser') is not True:
            return Response({"error": "is_superuser must be true"}, status=status.HTTP_400_BAD_REQUEST)

        return self.create_user(email, first_name, last_name, password, **other_fields)


USER_TYPE_CHOICES = (
    ('employer', 'Employer'),
    ('employee', 'Employee'),
    ('admin', 'Admin'),
)


class CustomUser(MainModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    role = models.CharField(choices=USER_TYPE_CHOICES,
                            max_length=30, default='employee')
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.first_name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


def build_profile_on_user_creation(sender, instance, created, **kwargs):
    if created:
        profile = Profile(owner=instance)
        profile.save()


post_save.connect(build_profile_on_user_creation, sender=CustomUser)


class Profile(MainModel, models.Model):
    owner = models.ForeignKey(
        to=CustomUser, on_delete=models.CASCADE, related_name='profile_owner')
    resume = models.FileField(null=True, blank=True)
    text_resume = models.TextField(null=True, blank=True)
    user_company_logo = models.ImageField(
        blank=True, upload_to='media', null=True)

    def __str__(self):
        return self.owner.first_name
