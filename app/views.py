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
    print('All Districts: ', all_districts)  

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

        userObject = request.user  # User vanni object lai userObject vanii variable ma rakheko so that hamiley tyo object dot garera disease_id  Usermodel ma add garna sakiyos vanera
        userObject.disease_id = disease_id  # hospital_User vanni table ma disease_id vanni field cha so tyo field ma user le choose gareko disease ko id store garayeko.

        userObject.save()


        patientObject = Patient()  # Patient vanni table ma yedi kei kura store garauna cha vani pahele tesko object banauna parcha.. i.e here it is 'patientObject'
        
        patientObject.name = patient_name  # table ko field ko ma kei kura insert garna cha vani yesari  baneko object i.e ('patientObject') dot ani field ko name ma hami user bata ayeko kura rakhdinchau
        patientObject.age = patient_age
        patientObject.location = patient_location
        patientObject.contact = patient_contact
        patientObject.blood_group = patient_bloodgroup
        patientObject.disease = patient_disease
        patientObject.user_id = request.user.id  # User Model ma vako particular logged in vako user ko id get garera tyo id lai Patient table ma rakheko as Patient Model and User Model are linked with each other with the help of user_id.
        
        print('Patient District Id: ', patient_district_id)
        district_obj = District.objects.filter(id=patient_district_id).first()
        patientObject.district = district_obj

        patientObject.save()

        diseaseById = request.user.disease_id  # User Model bata hamiley disease_id lai get gareko so that tyo 'disease_id' 'getRecommendation' vanni method ma pass garna ko lagi.
        
        hospitals = getRecommendations(diseaseById)  # Jaba yo method-> 'getRecommendation(diseaseById)' call huncha yesle particular user le kun disease search gareyko cha tesko id ko through disease liyera tyo disease ko hospital lai recommend gareko huncha..
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


    hospitals = getRecommendations(diseaseById)  # Jaba yo method-> 'getRecommendation(diseaseById)' call huncha yesle particular user le kun disease search gareyko cha tesko id ko through disease liyera tyo disease ko hospital lai recommend gareko huncha..
    # 'hospitals' vanni yeuta list ho jasma getRecommendation() method call hunda tyo method le return vareko values haru ayera baseko huncha.

    context = {'diseases': diseases, 'districts': all_districts, 'patient_disease': patient_disease, 'diseaseById': diseaseById, 'hospitals': hospitals}  # Key value pair ma hamiley context pass gareko so that it could be used in templates.

    return render(request, 'app/clienthome.html', context)






# Yo method sabsey important role play garcha. Yo method ko main target vaneko database ko Linker Table (i.e hospital_diesase_hospitals<= ManyToManyField() le create gardeko table) ma kam gareko cha..
def getRecommendations(diseaseById):
    hospitalById = list(Disease.hospitals.through.objects.filter(disease_id=diseaseById).values('hospital_id'))  # 1. Suru ma ta disease_id as a parameter auncha method call hunda. (method call clienthome() method bata vako cha..)
    
    # 2. Yo Query le  tyo ayeko 'disease_id' liyera Linker Table bata jati pani 'disease_id' gareko diseases haru cha tesbata hospitals haru nikalni kam gareko cha.[ .values('hospital_id') garera hospitals haru filterout gareko cha]
    # 3. Linker Table ma query chalauna at first:
    #			i) Model ma hererera ManyToManyField() kun Model name ma cha patta lagauna paryo => In our case it's in 'Disease' Model
    #			   tesailey query ko suru mai 'Disease' vanera haleko
    #			ii) Disease vanni model ma ManyToManyField() gareko field ko name 'hospitals' vanni cha tesailey query ma 'Disease.hospitals' vanera aako ho.
    #			iii) '.through' pani use garnai parcha kina ki Hami Linker Table ma kam gardai chau..
    # 4. Ayeko Queryset lai hami le 'list' ma convert gardiyeko so that haneko query bata ayeko hospital_id lai sajilai nikalna sakos vanera.
    # 5. IMP NOTEE: .values('hospital_id') le dictionary return gardincha so ava hamro 'hospitalById' vanni list vitra yeuta dictionary baseko huncha..

    # hospitalById<{'hospital_id':3}, {'hospital_id':4}, {'hospital_id':5}, {'hospital_id':6}>	#hospitalById query set ma exact yesari value ayerako huncha.

    recommended_hospital = []  # recommended_hospital yeuta khali list create gareko..
    
    for i in range(len(hospitalById)):  # 'hospitalById' aba yeuta as a list jasto vitra values haru chai as  a dictionary ko rup ma baseko huncha so tesma loop chalayeko.
        
        recommended_hospital.append(hospitalById[i]['hospital_id'])  # 'hospitalById' vanni list vitra ko dictionary bata hamilai aba key chaindaina tara 'values' haru chai chaini vako le yesto gareko => "hospitalById[i]['hospital_id']". yo dictionary ma hareko values ko key vaney feri 'hospital_id' nai baseko huncha..
    
    # tespachi loop bata jati ni values haru ayeko cha teslai recommended_hospital vanni list ma append gardeko.. append garena vani loop bata ayeko last ko values matra gayera bascha..


    hospitals = []  # yeuta hospitals vanni khali list create gareko.
    
    for i in range(len(recommended_hospital)):  # ahiley sama ta 'recommended_hospital' list ma hospital ko id matrai baseko cha. Aba hamilai tyo hospital ko id ko through hamilai hospital ko name chayeko cha so loop lagayera 'Hospital' table ma hospital ko name haru nilakera 'hospitals' vanni list ma rakheko ho
        
        hospitals += Hospital.objects.filter(id=recommended_hospital[i])
    
    
    return hospitals  # Yesle method call hunda 'hospitals' vanni list lai return garcha jasma hamro particular patient lai lageko ko disease ko adhar ma hospitals haru ayera baseko huncha..











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




