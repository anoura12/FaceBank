from .models import Face, MoneyTransfer
from django.forms import ModelForm  
from django import forms
from django.contrib.auth.forms import AuthenticationForm
  
  
class UserImageForm(ModelForm):  
    class Meta:  
        model = Face  
        fields = '__all__'  

class MoneyTransferForm (ModelForm): #form for capturing transaction details
    class Meta:
        model = MoneyTransfer
        fields = '__all__'


class UserLoginForm(AuthenticationForm): #form for capturing login details
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={
             'class': 'your-class',
             'placeholder': 'Enter your username',
             'id': 'username-input'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'your-class'}))