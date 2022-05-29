from django.db import models  
from django.forms import fields  
from .models import Face, MoneyTransfer
from django.forms import ModelForm  
  
  
class UserImageForm(ModelForm):  
    class Meta:  
        model = Face  
        fields = '__all__'  

class MoneyTransferForm (ModelForm):
    class Meta:
        model = MoneyTransfer
        fields = '__all__'