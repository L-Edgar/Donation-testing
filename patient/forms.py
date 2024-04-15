from django import forms
from django.contrib.auth.models import User
from . import models
from django.forms import PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import TextInput


class PatientUserForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].required=False

class PatientForm(forms.ModelForm):
    
    class Meta:
        model=models.Patient
        fields=['age','bloodgroup','disease','address','doctorname','mobile','profile_pic']

#class PatientLoginForm(forms.ModelForm):
    
  #  class Meta:
    #    model=models.Patient
  #      fields=['username','password']
   #     widgets = {
   #     'password': forms.PasswordInput()
   #     }
        

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

