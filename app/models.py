from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator



class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(
        upload_to='uploads/',
        null=True,
        blank=True,
        default='uploads/img_avatar.png'
    )
    disease = models.ForeignKey('Disease', null=True, blank=True, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now, null=True)


class Hospital(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    phone = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.FileField(blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name 


class Disease(models.Model):
    name = models.CharField(max_length=200)
    hospitals = models.ManyToManyField('Hospital', blank=True)

    def __str__(self):
        return self.name 


class District(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name 


class Patient(models.Model):
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=200, blank=True, null=True, validators=[MaxValueValidator(100), MinValueValidator(1)])
    district = models.ForeignKey('District', blank=True, null=True, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    contact = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=200, blank=True, null=True)
    disease = models.CharField(max_length=200, blank=True, null=True)
    inqury_date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Rate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey('Hospital', null=True, blank=True, on_delete=models.CASCADE)
    rating = models.FloatField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return self.user.username
