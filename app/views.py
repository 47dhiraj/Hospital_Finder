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

from app.models import Disease
from app.models import Surg
from app.models import Patient
from app.models import Hospital
from app.models import Rate
from app.models import District

import sweetify

from .forms import CreateClientForm
from .tokens import account_activation_token
from .decorators.authorize_decorators import role_required

from .utils.coordinate_finder import geocode_address, extract_lat_lng
from .utils.recommendation import recommendations_by_disease, recommendations_by_surgery, recommendation_by_distance

User = get_user_model()






# ---------------- Landing / Home page ----------------
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







# ---------------- Client Home & Recommendation page ----------------
@role_required(['is_client'], url='login')
def clienthome(request):
    user = request.user

    all_diseases = Disease.objects.all()
    all_surgeries = Surg.objects.all()
    all_districts = District.objects.all()

    # patient = request.user.patients.order_by('id').last()
    # patient = request.user.patients.order_by('inqury_date').last()
    patient = request.user.patients.latest('id')

    patient_disease = patient.disease if patient else None
    patient_surgery = patient.surgery if patient else None


    if request.method == 'GET' and patient_disease is None and patient_surgery is None:

        context = {
            'diseases': all_diseases,
            'surgeries': all_surgeries,
            'districts': all_districts,
        }
        return render(request, 'app/clienthome.html', context)


    elif request.method == 'GET':

        recommended_hospitals = []

        if patient_disease and not patient_surgery:
            recommended_hospitals = recommendations_by_disease(patient_disease)

        if patient_surgery and not patient_disease:
            recommended_hospitals = recommendations_by_surgery(surgery)

        recommended_hospitals = recommendation_by_distance(recommended_hospitals, patient.latitude, patient.longitude)

        context = {
            'diseases': all_diseases,
            'surgeries': all_surgeries,
            'districts': all_districts,
            
            'hospitals': recommended_hospitals,

            'selected_district_id': patient.district.id if patient.district else None,

            'selected_disease_id': patient.disease.id if patient.disease else None,
            'selected_disease_name': patient.disease.name if patient.disease else None,

            'selected_surgery_id': patient.surgery.id if patient.surgery else None,
            'selected_surgery_name': patient.surgery.name if patient.surgery else None,

            'selected_type': 'disease' if patient.disease else ('surgery' if patient.surgery else None),

            'entered_name': patient.name,
            'entered_age': patient.age,
            'entered_location': patient.location,
            'entered_contact': patient.contact,
            'entered_bloodgroup': patient.blood_group,
        }

        return render(request, 'app/clienthome.html', context)


    if request.method == 'POST':

        patient_name = request.POST.get('p_name', '').strip()
        patient_age = request.POST.get('p_age', '').strip()
        patient_location = request.POST.get('p_location', '').strip()
        patient_contact = request.POST.get('p_contact', '').strip()
        patient_bloodgroup = request.POST.get('bloodgroup', '').strip()

        district_raw = request.POST.get('p_district', '').strip()
        try:
            patient_district_id = int(district_raw)
        except (ValueError, TypeError):
            patient_district_id = None

        disease_raw = request.POST.get('disease', '').strip()
        surgery_raw = request.POST.get('surgery', '').strip()
        disease_id = None
        patient_disease = None
        surgery_id = None
        patient_surgery = None

        ## ---- If Disease selected ----
        if disease_raw and "-" in disease_raw:
            try:
                d_id, d_name = disease_raw.split('-', 1)
                disease_id = int(d_id)
                patient_disease = d_name.strip()

            except (ValueError, TypeError):
                disease_id = None
                patient_disease = None

        ## ---- If Surgery selected ----
        elif surgery_raw and "-" in surgery_raw:
            try:
                s_id, s_name = surgery_raw.split('-', 1)
                surgery_id = int(s_id)
                patient_surgery = s_name.strip()

            except (ValueError, TypeError):
                surgery_id = None
                patient_surgery = None
        

        ## Fetching District Object Safely
        district = None
        if patient_district_id:
            try:
                district = District.objects.get(id=patient_district_id)
            except District.DoesNotExist:
                district = None
        
        ## Fetching Disease Object Safely
        disease = None
        if disease_id:
            try:
                disease = Disease.objects.get(id=disease_id)
            except Disease.DoesNotExist:
                disease = None

        ## Fetching Surgery Object Safely
        surgery = None
        if surgery_id:
            try:
                surgery = Surg.objects.get(id=surgery_id)
            except Surg.DoesNotExist:
                surgery = None


        full_address = f"{patient_location}, {district.name}, Nepal"
        response = geocode_address(full_address)
        patient_latitude, patient_longitude = extract_lat_lng(response)

        # Fallback to district level address, only if latitude and longitude is None or missing
        if patient_latitude is None or patient_longitude is None:
            fallback_address = f"{district.name}, Nepal"
            response = geocode_address(fallback_address)
            patient_latitude, patient_longitude = extract_lat_lng(response)
        
        ## Creating a new patient object
        patient = Patient.objects.create(
            name=patient_name,
            age=patient_age,
            location=patient_location,
            latitude=patient_latitude,
            longitude=patient_longitude,
            contact=patient_contact,
            blood_group=patient_bloodgroup,
            user=user,
            disease=disease,
            surgery=surgery,
            district=district
        )

        recommended_hospitals = []

        if disease and not surgery:
            recommended_hospitals = recommendations_by_disease(disease)

        if surgery and not disease:
            recommended_hospitals = recommendations_by_surgery(surgery)

        if recommended_hospitals and patient_latitude and patient_longitude:
            recommended_hospitals = recommendation_by_distance(recommended_hospitals, patient_latitude, patient_longitude)

        context = {
            'diseases': all_diseases,
            'surgeries': all_surgeries,
            'districts': all_districts,
            'hospitals': recommended_hospitals,
            'selected_district_id': district.id if district else None,
            'selected_disease_id': disease.id if disease else None,
            'selected_disease_name': disease.name if disease else None,
            'selected_surgery_id': surgery.id if surgery else None,
            'selected_surgery_name': surgery.name if surgery else None,
            'selected_type': 'disease' if disease else ('surgery' if surgery else None),
            'entered_name': patient_name,
            'entered_age': patient_age,
            'entered_location': patient_location,
            'entered_contact': patient_contact,
            'entered_bloodgroup': patient_bloodgroup,
        }

        return render(request, 'app/clienthome.html', context)






# ---------------- Admin Dashboard page ----------------
@role_required(['is_admin'], url='login')
def adminhome(request):

    context = {}

    return render(request, 'app/adminhome.html', context)




# ---------------- Hospital Detail page ----------------
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






# ---------------- Client Deail page ----------------
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

