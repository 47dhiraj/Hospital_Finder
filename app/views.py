from django.conf import settings

from .models import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone



from django.core.mail import send_mail
from django.core.mail import EmailMessage


import sweetify


from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

## latest modification
from django.utils.encoding import force_bytes, force_str


import datetime
from datetime import timedelta



# Create your views here.


def home(request):
    
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact_detail = "\n Name: " + name + "\n Email: " + email + "\n\n Message: " + message

        if not request.user.is_authenticated:
            subject = "A Visitor's Comment"
        else:
            subject = str(request.user) + "'s Comment"


        send_mail(
            subject=subject,
            message=contact_detail,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
 
 
        messages.success(request, ' Thank you for getting in touch! ')


    return render(request, 'app/index.html')


