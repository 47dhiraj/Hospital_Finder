from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError


User = get_user_model()



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
        user.is_active = False   # user must activate via email
        user.is_client = True
        user.is_admin = False
        if commit:
            user.save()
        return user

