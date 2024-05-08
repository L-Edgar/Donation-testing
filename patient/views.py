from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from django.contrib.auth import login, authenticate
from blood import models as bmodels
from django.contrib import messages
#from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout
from django.http import Http404

def loginView(request):
    messages.success(request,'')
    print(f"Request method: {request.method}")
    if request.method=='POST':
        login_form=forms.PatientUserForm(request.POST)
        username=request.POST['username']
        password=request.POST['password']
        
        user = authenticate(request, username=username, password=password,role='patient',model=models.CustomUser)
        #if login_form.is_valid():
            #username=login_form.cleaned_data['username']
            #password=login_form.cleaned_data['password']
            
            
            
        if user is not None and user.role == 'patient':
            login(request,user)
            return redirect('patient:patient-dashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('patient:patientlogin')
            
        #else:
            #print(f"Form errors: {login_form.errors}")
            
    else:
        login_form = forms.PatientUserForm()  # An unbound form
        print("unsuccessful")
        
    return render(request,'patient/patientlogin.html',{'login_form':login_form})



def logout_view(request):
    auth_logout(request)
    return render(request,"blood/logout.html")

def patient_signup_view(request):
    #userForm=forms.PatientUserForm()
    #patientForm=forms.PatientForm()
    #mydict={'userForm':userForm,'patientForm':patientForm}
    userForm=forms.CustomUserCreationForm()
    
    
    if request.method=='POST':
        userForm=forms.CustomUserCreationForm(request.POST)
        #userForm=forms.PatientUserForm(request.POST)
        #patientForm=forms.PatientForm(request.POST,request.FILES)
        
            
        if userForm.is_valid():
            password1=userForm.cleaned_data['password1']
            password2=userForm.cleaned_data['password2']
            username=userForm.cleaned_data['username']
            print("Form is valid")
            
            if password1==password2:
                 
                 if forms.CustomUserCreationForm.Meta.model.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists.')
                    print("Username already exists")
                    return render(request, 'patient/patientsignup.html', {'userForm': userForm})
                    
                 else:
                    user = userForm.save(commit=False)
                    user.role = 'patient'
                    userForm.save()
                    #user.set_password(user.password)
                    print("successfull")
                    
                #patient=patientForm.save(commit=False)
                #patient.user=user
                #patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
                #patient.save()
                #my_patient_group = Group.objects.get_or_create(name='PATIENT')
                #my_patient_group[0].user_set.add(user)
                    return redirect('patient:patientlogin')
            else:
                messages.info(request,"Passwords do not match.")
                return redirect('patient:patientsignup')

        else:
            print(userForm.errors)
    else:
        userForm=forms.CustomUserCreationForm()
        print('Error 3', userForm.errors)
    return render(request,'patient/patientsignup.html',{'userForm': userForm})

def complete_registration(request):
    patient=models.Patient.objects.filter(user_id=request.user.id).first()
    if request.method=='POST':
        user_form=forms.PatientForm(request.POST,instance=patient)
        if user_form.is_valid():
            print("Third User:", request.user)
            user_form.instance.user = request.user
            user_form.save()
            print("Successful")
            redirect_url = request.GET.get('next', 'patient:patient-dashboard')
            return redirect(redirect_url)
            

        else:
            print("Error: ", user_form.errors)
            print("Second User:", request.user)

    else:
        user_form = forms.PatientForm(instance=patient)
    return render(request,"patient/patient_registration.html",{'user_form':user_form})

@login_required(login_url='patientlogin')
def patient_dashboard_view(request):
    patient=models.Patient.objects.filter(user_id=request.user.id).first()
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),

    }
   
    return render(request,'patient/patient_dashboard.html',context=dict)

@login_required(login_url='patientlogin')
def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            patient= models.Patient.objects.filter(user_id=request.user.id).first()
            blood_request.request_by_patient=patient
            blood_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'patient/makerequest.html',{'request_form':request_form})

@login_required(login_url='patientlogin')
def my_request_view(request):
    try:
        patient= get_object_or_404(models.Patient, user_id=request.user.id)
        if not (patient.bloodgroup or patient.doctorname or patient.disease or patient.age):
            return redirect('patient:complete-reg')
        blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
        return render(request,'patient/my_request.html',{'blood_request':blood_request})
    except Http404:
        return redirect('patient:complete-reg')



@login_required(login_url='patientlogin')
def patient_profile(request):
    patient=models.Patient.objects.filter(user_id=request.user.id).first()
    return render(request,'patient/patient_profile.html',{'patient':patient})