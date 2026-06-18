from django.db import models

# Create your models here.

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import CharField, DecimalField, Model, CASCADE, ForeignKey, ImageField, TextField, DateTimeField, \
    IntegerField, SmallIntegerField, EmailField , BooleanField, FloatField


class CustomUserManager(UserManager):

    def _create_user_object(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The given phone must be set")
        phone = self.normalize_email(phone)
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        return user

    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given  phone, and password.
        """
        user = self._create_user_object(phone, password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    class Status(models.TextChoices):
        PASSENGER = 'passenger','Passenger'
        DRIVER = 'driver','Driver'
        ADMIN = 'admin','Admin'
    username = None
    password = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    phone = CharField(unique=True, max_length=20)
    status = CharField(choices=Status.choices,  max_length=20)
    language = CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    email = EmailField()


class City(Model):
    name = CharField(max_length=50)
    viloyat = CharField(max_length=50)
    latitude = DecimalField(max_digits=9, decimal_places=6)
    longitude = DecimalField(max_digits=9, decimal_places=6)
# Hello

class Route(Model):
    class Type(models.TextChoices):
        SEDAN = 'sedan','Sedan'
        MONOVOLUME = 'monovolume','Monovolume'
    class Status(models.TextChoices):
        FAOL = 'faol','Faol'
        YOPIQ = 'yopiq','Yopiq'
    driver = ForeignKey('apps.Driver', on_delete=CASCADE, related_name='routes')
    from_city = CharField(max_length=50)
    to_city = CharField(max_length=50)
    leave_time = DateTimeField()
    price = DecimalField(max_digits=9, decimal_places=6)
    free_seats = IntegerField()
    car_type = CharField(choices=Type.choices,default=Type.SEDAN ,max_length=50)
    status = CharField(choices=Status.choices,default=Status.YOPIQ ,max_length=50)

class Driver(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='drivers')
    car_mark = CharField(max_length=25)
    car_model = CharField(max_length=25)
    car_number = CharField(max_length=25)
    prava_image = ImageField(upload_to='prava/')
    prava_confirm = BooleanField()
    reyting = FloatField()
    travel_count = SmallIntegerField(blank=True, null=True, default=0)


class Booking(Model):
    route = ForeignKey('apps.Route' , on_delete=CASCADE)
    passenger = ForeignKey('apps.User' , on_delete=CASCADE)
    seats_number = models.SmallIntegerField()
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(Model):
    booking = ForeignKey('apps.Booking' , on_delete=CASCADE)
    reviewer = ForeignKey('apps.User' , on_delete=CASCADE)
    reviewed = ForeignKey('apps.Driver' , on_delete=CASCADE)
    score = models.FloatField()
    destination = models.TextField()