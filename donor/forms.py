from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()



class DonorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['password'].required=False

class DonorForm(forms.ModelForm):
    class Meta:
        model=models.Donor
        fields=['bloodgroup','address','mobile','profile_pic','date_of_birth']

   # user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput())
   # def __init__(self, *args, **kwargs):
    #    user = kwargs.pop('user', None)
    #    super(DonorForm, self).__init__(*args, **kwargs)

    #    if user:
     #       self.fields['user'].initial = user
     #       self.fields['user'].widget.attrs['disabled'] = True 

    #def save(self, commit=True):
    #    instance = super(DonorForm, self).save(commit=False)
    #    instance.user = self.cleaned_data['user']
    #    if commit:
     #       instance.save()
     #   return instance

class DonationForm(forms.ModelForm):
    class Meta:
        model=models.BloodDonate
        fields=['age','bloodgroup','disease','unit']


class CustomUserCreationForm(UserCreationForm):
    role = forms.CharField(max_length=20, initial='donor',required=False) 
    class Meta:
        model =CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'role']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(render_value=True)
        self.fields['password2'].widget = forms.PasswordInput(render_value=True)
   

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user