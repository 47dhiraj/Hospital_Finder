from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm  # UserCreationForm  import garnu ko karan vaneko yesle djagno le
                                                        # User ko lagi diyeko authentication form automatic dinxa... yo form use garyo vani password lai 
                                                        # manually hash garnu pardaina... django le automatic hash gardinxa  & Username pahilai nai use vako
                                                        # xa ki nai vanera check garne code lekhnu parena ... django le automatic check gardinxa
from django.contrib.auth.models import User  # yaha User vaneko django le diyeko inbuilt User model ho
from django import forms  # forms.py page ma yo forms vanni import garnai parxa
from django.db import transaction
from .models import *
from django.core.exceptions import ValidationError





class CreateClientForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            "username": None,
            "email": None,
            "password2": None,
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("User with this email already exists.")
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False       # inactive until email confirmation
        user.is_client = True        # custom field
        user.is_admin = False        # custom field
        if commit:
            user.save()
        return user