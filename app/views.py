from django.conf import settings

from .models import *

from .forms import CreateClientForm

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

from .tokens import account_activation_token



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






def clientregisterPage(request):
    
    form = CreateClientForm()

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)


    if request.method == 'POST':
        
        form = CreateClientForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)

            # Prepare activation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account -- Hospital Finder'
            message = render_to_string('app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            messages.success(request, f'Account activation link has been sent to {to_email}!')

            return redirect('clienthome')


    context = {'form': form}
    return render(request, 'app/register.html', context)





def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()

        login(request, user)  # auto login

        messages.success(request, "Your account has been activated!")
        
        return redirect('clienthome')
    
    else:
        return HttpResponse('Activation link is invalid!')
    