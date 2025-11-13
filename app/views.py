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
from django.core.mail import EmailMessage
from django.conf import settings


from .models import *

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
    
    return render(request, 'app/index.html')


