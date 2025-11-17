from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

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

from app.models import Disease
from app.models import Patient
from app.models import Hospital
from app.models import Rate
from app.models import District



from .utils.coordinate_finder import geocode_address
from .utils.distance_calculator import calculate_distance_in_km



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
    
    diseases = Disease.objects.all()  # Disease table bata j jati kura cha tyo sabai lai get garera 'disease' vanni object ma haleko. Yo Query kina gareko vanda yesle template ma drop down ma database ma jun jun disease cha tyo sabai list out garna help gareko cha.
    
    all_districts = District.objects.all()
    # print('All Districts: ', all_districts)  




    # Post method
    if request.method == 'POST':

        patient_name = request.POST['p_name']
        patient_age = request.POST['p_age']
        patient_district_id = int(request.POST.get('p_district', '').strip())
        patient_location = request.POST['p_location']
        patient_contact = request.POST['p_contact']
        patient_bloodgroup = request.POST['bloodgroup']
        disease_id, patient_disease = request.POST['disease'].split('-')  # select option ko value and text both chaiyo vani yesari split garera liencha.
        # ALTERNATIVE CODE # disease_id = request.POST['disease']

        disease_obj = Disease.objects.get(id=disease_id)
        
        userObject = request.user

        userObject.disease = disease_obj

        userObject.save(update_fields=['disease']) 


        patientObject = Patient()  # Patient vanni table ma yedi kei kura store garauna cha vani pahele tesko object banauna parcha.. i.e here it is 'patientObject'
        
        patientObject.name = patient_name  # table ko field ko ma kei kura insert garna cha vani yesari  baneko object i.e ('patientObject') dot ani field ko name ma hami user bata ayeko kura rakhdinchau
        patientObject.age = patient_age
        patientObject.location = patient_location
        patientObject.contact = patient_contact
        patientObject.blood_group = patient_bloodgroup
        patientObject.disease = patient_disease
        patientObject.user_id = request.user.id  # User Model ma vako particular logged in vako user ko id get garera tyo id lai Patient table ma rakheko as Patient Model and User Model are linked with each other with the help of user_id.
        
        district_obj = District.objects.filter(id=patient_district_id).first()

        patientObject.district = district_obj

        full_address = patient_location + ", " + district_obj.name + ", Nepal"
        response = geocode_address(full_address)

        patient_latitude = response['data']['lat']
        patient_longitude = response['data']['lng']

        patientObject.latitude = patient_latitude
        patientObject.longitude = patient_longitude

        patientObject.save()
   


        diseaseById = request.user.disease_id  # User Model bata hamiley disease_id lai get gareko so that tyo 'disease_id' 'getRecommendation' vanni method ma pass garna ko lagi.
        
        hospitals = get_recommendations_by_disease(diseaseById)  # Jaba yo method-> 'get_recommendations_by_disease(diseaseById)' call huncha yesle particular user le kun disease search gareyko cha tesko id ko through disease liyera tyo disease ko hospital lai recommend gareko huncha..
        # 'hospitals' vanni yeuta list ho jasma getRecommendation() method call hunda tyo method le return vareko values haru ayera baseko huncha.

        context = {'diseases': diseases, 'districts': all_districts, 'patient_disease': patient_disease, 'diseaseById': diseaseById, 'hospitals': hospitals}  # Key value pair ma hamiley context pass gareko so that it could be used in templates.

        return render(request, 'app/clienthome.html', context)






    # Code for GET Method
    diseaseById = request.user.disease_id  # Yo Query le User Model bata pahele particular user ko 'disease_id' vanni field linxa and tyo field ma user le search gareko disease ko id ayera baseko huncha


    if diseaseById is None:  # Yo if condition kina lagauna parcha ta vanda... Yedi kunai user chai first time login gardai cha (i.e new user )cha vani User Model ma 'disease_id' suruma NULL vako huncha so tyo case check garna parcha natra error falxa.
        
        context = {'diseases': diseases, 'districts': all_districts,}  # Yo 'diseases' vani line no. 89 mai get gareko cha so yo line le template ma disease name haru pass gardeko matrai ho becz hamailai disease name dropdown ma dekhauna cha..
        
        return render(request, 'app/clienthome.html', context)

    else:
        patient_disease = Disease.objects.get(id=diseaseById)  # Disease vanni Model ma  User model bata ayeko 'disease_id' (diseaseById) lai pass garera particular disease name nikaleko so that yo chai template ma "Hospital Recommendation For {{patient_disease}}" vanera garna pawos vanera gareko..


    hospitals = get_recommendations_by_disease(diseaseById)  # Jaba yo method-> 'get_recommendations_by_disease(diseaseById)' call huncha yesle particular user le kun disease search gareyko cha tesko id ko through disease liyera tyo disease ko hospital lai recommend gareko huncha..
    # 'hospitals' vanni yeuta list ho jasma getRecommendation() method call hunda tyo method le return vareko values haru ayera baseko huncha.

    context = {'diseases': diseases, 'districts': all_districts, 'patient_disease': patient_disease, 'diseaseById': diseaseById, 'hospitals': hospitals}  # Key value pair ma hamiley context pass gareko so that it could be used in templates.

    return render(request, 'app/clienthome.html', context)







def get_recommendations_by_disease(diseaseById):

    # print('Disease ID: ', diseaseById)
    
    disease = Disease.objects.get(id=diseaseById)

    hospitals = disease.hospitals.all()

    return list(hospitals)











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




def logoutall(request):

    if request.method == "POST":

        logout(request)
        
        return redirect('login')
    
    return redirect('home')







def demo_map_page(request):

    context = {"google_maps_api_key": settings.GOOGLE_MAPS_API_KEY}

    return render(request, "app/map.html", context)

