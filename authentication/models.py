from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    ADMIN="AD"
    STAFF="ST"
    CUSTOMER="CU"
    role_choices=[(ADMIN,"admin"),(STAFF,"staff"),(CUSTOMER,"customer")]
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=2,choices=role_choices,default=CUSTOMER)
