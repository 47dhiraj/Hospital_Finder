from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower





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
    date_joined = models.DateTimeField(default=timezone.now, null=True)






class Hospital(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(100),
        ]
    )
    location = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    images = models.FileField(blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='unique_hospital_name',
            ),
        ]






class Disease(models.Model):
    name = models.CharField(
        max_length=120, 
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(120),
        ]
    )

    hospitals = models.ManyToManyField('Hospital', blank=True)


    def __str__(self):
        return self.name
    

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='unique_disease_name',
            ),
        ]






class Surg(models.Model):
    
    name = models.CharField(
        max_length=100, 
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(100),
        ]
    )

    hospitals = models.ManyToManyField('Hospital', blank=True)


    def __str__(self):
        return self.name
    

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='unique_surgery_name',
            ),
        ]





class District(models.Model):

    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(4),   
            MaxLengthValidator(50),
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='unique_district_name',
            ),
        ]




class Patient(models.Model):
    
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=200, blank=True, null=True, validators=[MaxValueValidator(100), MinValueValidator(1)])
    location = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    blood_group = models.CharField(max_length=200, blank=True, null=True)

    inqury_date = models.DateTimeField(auto_now_add=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='patients')
    
    disease = models.ForeignKey('Disease', blank=True, null=True, on_delete=models.CASCADE)
    
    surgery = models.ForeignKey('Surg', blank=True, null=True, on_delete=models.CASCADE)
    
    district = models.ForeignKey('District', blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.name




class Rate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    hospital = models.ForeignKey('Hospital', null=True, blank=True, on_delete=models.CASCADE)
    rating = models.FloatField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])

    def __str__(self):
        return self.user.username

