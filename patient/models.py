from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('donor', 'Donor'),
        ('admin','Blood')
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='user permissions',
    )

class Patient(models.Model):
    
    

    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Patient/',null=True,blank=True)
    
    age=models.PositiveIntegerField()
    bloodgroup=models.CharField(max_length=10)
    disease=models.CharField(max_length=100)
    doctorname=models.CharField(max_length=50)

    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    disease=models.CharField(max_length=100,default="Nothing")
   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name