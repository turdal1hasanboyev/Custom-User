from django.db import models
import re
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
        def create_user(self, phone_number, email, password=None, **extra_fields):
            if not phone_number:
                raise ValueError("Telefon raqami kiritilishi shart")
            if password is None:
                raise ValueError("Parol kiritilishi shart")
            if not re.match(r'^\+?[0-9]{10,15}$', phone_number):
                raise ValueError("Telefon raqami noto'g'ri formatda. Masalan: +998901234567")
            if not email:
                raise ValueError("Email kiritilishi shart")
            
            email = self.normalize_email(email)

            user = self.model(phone_number=phone_number, email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        
        def create_superuser(self, email, password=None, phone_number=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)

            if extra_fields.get('is_staff') is not True:
                raise ValueError("Superuser uchun is_staff=True bo'lishi shart.")
            if extra_fields.get('is_superuser') is not True:
                raise ValueError("Superuser uchun is_superuser=True bo'lishi shart.")
            if phone_number is None:
                raise ValueError("Superuser uchun telefon raqami kiritilishi shart.")
            if password is None:
                raise ValueError("Superuser uchun parol kiritilishi shart.")
            if not re.match(r'^\+?[0-9]{10,15}$', phone_number):
                raise ValueError("Telefon raqami noto'g'ri formatda. Masalan: +998901234567")
            if not email:
                raise ValueError("Superuser uchun email kiritilishi shart.")
            
            user = self.create_user(phone_number=phone_number, email=email, password=password, **extra_fields)
            return user


class CustomUser(AbstractUser):
    GENDER = (
        ('Male', ('Male')),
        ('Female', ('Female')),
    )
    username = None
    email = models.EmailField(unique=True, db_index=True, max_length=225, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="Images/", null=True, blank=True, default='img/default.png')
    video = models.FileField(upload_to="Videos/", null=True, blank=True)
    phone_number = models.CharField(max_length=225, null=True, blank=True, unique=True)
    adress = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=225, choices=GENDER, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        if self.get_full_name():
            return f"{self.id}-{self.get_full_name()}"
        if self.email:
            return f"{self.id}-{self.email}"
        return f"{self.id}-{self.phone_number}"