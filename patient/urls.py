from django.urls import path

#from django.contrib.auth.views import LoginView
from . import views

app_name='patient'
urlpatterns = [
    #path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html'),name='patientlogin'),
    path('patientlogin',views.loginView,name='patientlogin'),
    path('patientlogout',views.logout_view,name='logout'),
    path('patientsignup', views.patient_signup_view,name='patientsignup'),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('make-request', views.make_request_view,name='make-request'),
    path('my-request', views.my_request_view,name='my-request'),
    path('patient-profile',views.patient_profile,name='patient-profile'),
    path('complete-reg',views.complete_registration,name="complete-reg")
]