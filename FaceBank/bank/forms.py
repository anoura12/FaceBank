from django.db import models  
from django.forms import fields  
from .models import Face
from django.forms import ModelForm  
  
  
class UserImageForm(ModelForm):  
    class Meta:  
        # To specify the model to be used to create form  
        model = Face 
        # It includes all the fields of model  
        fields = '__all__'  