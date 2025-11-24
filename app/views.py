from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.mail import EmailMessage, send_mail

from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string

from django.utils.encoding import force_bytes, force_str

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth import get_user_model

from .forms import CreateClientForm

from .tokens import account_activation_token


from .decorators.authorize_decorators import role_required

from app.models import Disease
from app.models import Surg
from app.models import Patient
from app.models import Hospital
from app.models import Rate
from app.models import District


import sweetify


from .utils.coordinate_finder import geocode_address, extract_lat_lng
from .utils.distance_calculator_geopy import calculate_distance_in_km_with_geopy

from .utils.distance_calculator_haversine import calculate_distance_with_haversine





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

            sweetify.success(request, f'You are logged in !', text= f'Welcome back, {username}.', persistent=False, icon='success', timer=2000)
            
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




@role_required(['is_client'], url='login')
def clienthome(request):
    
    diseases = Disease.objects.all()
    surgeries = Surg.objects.all()
    all_districts = District.objects.all()


    patient = request.user.patients.order_by('inqury_date').last()
    print('Patient: ', patient)

    patient_disease = patient.disease if patient else None
    print('Patient Disease: ', patient_disease)


    if patient_disease is None:
        context = {'diseases': diseases, 'surgeries': surgeries, 'districts': all_districts,}
        return render(request, 'app/clienthome.html', context)
    







def get_recommendations_by_disease(diseaseById):

    # print('Disease ID: ', diseaseById)
    
    disease = Disease.objects.get(id=diseaseById)

    hospitals = disease.hospitals.all()

    return list(hospitals)





def get_recommendation_by_distance(hospitals, patient_latitude, patient_longitude):

    """
        Sort hospitals based on distance to patient.
    """

    hospital_distances = []

    for hospital in hospitals:

        ## To calculate distance using Haversine Algorith / Formula
        distance = calculate_distance_with_haversine(
            patient_latitude,
            patient_longitude,
            hospital.latitude,
            hospital.longitude,
            unit="km"
        )


        ## To calculate distance using geopy
        # distance = calculate_distance_in_km_with_geopy(
        #     patient_latitude,
        #     patient_longitude,
        #     hospital.latitude,
        #     hospital.longitude
        # )


        # print('\nDistance: ', distance, ' Type; ', type(distance))


        ## making hospital_distances a list of tuples e.g (hospital_1, 10)
        hospital_distances.append((hospital, distance))

    
    hospital_distances.sort(key = lambda item: item[1])                         # item[0] represent single hospital_object and item[1] is a distance from patient to that paritcular hospital.

    return [hospital_ojects[0] for hospital_ojects in hospital_distances]       # Return sorted hospital objects





@role_required(['is_admin'], url='login')
def adminhome(request):

    context = {}

    return render(request, 'app/adminhome.html', context)





def detail(request, hospital_id):

    hospital = get_object_or_404(Hospital, id=hospital_id)

    if request.method == "POST":

        rate = request.POST['rating']
        rateObject = Rate()
        rateObject.user = request.user
        rateObject.hospital = hospital
        rateObject.rating = rate

        rateObject.save()

        messages.success(request, "Your Rating has been submited.")

    context = {'hospital': hospital}
    
    return render(request, 'app/detail.html', context)



@role_required(['is_admin'], url='login')
def customerdetail(request):

    users = User.objects.all().order_by('id')

    context = {'users': users}

    return render(request, 'app/customerdetail.html', context)





# Find hospital function to display all the hospitals.
def findHospital(request):

    query = request.GET.get('searchvalue')

    if query:

        hospital = Hospital.objects.filter(Q(name__icontains=query)).distinct()

        context = {'hospital_list': hospital}

        return render(request, 'app/hospital_list.html', context)


    hospital_list = Hospital.objects.all()

    context = {'hospital_list': hospital_list}

    return render(request, 'app/hospital_list.html', context)



@login_required
def logoutall(request):

    if request.method == "POST":
        logout(request)
        sweetify.success(request, 'You are logged out !', text=f'Bye {request.user.username}, see you soon.', persistent=False, icon='success', timer=1500)
        return redirect('home')
    
    
    return redirect('home')







# def demo_map_page(request):

#     context = {"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY}

#     return render(request, "app/map.html", context)

