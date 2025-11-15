from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .forms import CreateClientForm
from .tokens import account_activation_token
from django.conf import settings

User = get_user_model()



def home(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact_detail = f"\n Name: {name}\n Email: {email}\n\n Message: {message}"
        subject = f"{request.user}'s Comment" if request.user.is_authenticated else "A Visitor's Comment"

        send_mail(
            subject=subject,
            message=contact_detail,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        messages.success(request, 'Thank you for getting in touch!')

    return render(request, 'app/index.html')





# ---------------- Registration ----------------
def clientregisterPage(request):

    form = CreateClientForm()

    if request.method == 'POST':

        form = CreateClientForm(request.POST)

        if form.is_valid():
            user = form.save()
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

            messages.success(request, f'Activation link sent to {to_email}!')

            return redirect('login')


    return render(request, 'app/register.html', {'form': form})





# ---------------- Activation ----------------
def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None


    if user and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()
        login(request, user)  # auto login after activation

        messages.success(request, "Account activated successfully!")

        if user.is_client:
            return redirect('clienthome')
        else:
            return redirect('adminhome')
        
    else:
        
        return render(request, 'app/activation_invalid.html')



# ---------------- Login ----------------
def loginPage(request):

    if request.user.is_authenticated:

        if request.user.is_client:
            return redirect('clienthome')
        else:
            return redirect('adminhome')


    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:

            login(request, user)
            
            if user.is_client:
                return redirect('clienthome')
            else:
                return redirect('adminhome')
        else:
            # Check if user exists but inactive
            try:
                temp_user = User.objects.get(username=username)
                if not temp_user.is_active:
                    messages.warning(request, "Your account is inactive. Please activate via email.")
            except User.DoesNotExist:
                pass
            messages.error(request, 'Invalid username or password!')

    return render(request, 'app/login.html')





def clienthome(request):
    return render(request, 'app/clienthome.html')



def adminhome(request):
    return render(request, 'app/adminhome.html')
