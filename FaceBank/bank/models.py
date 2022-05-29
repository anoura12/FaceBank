from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Face(models.Model):
    username = models.CharField(max_length=50)
    face = models.ImageField(upload_to='images/')

def __str__(self):
        return self.username

class MoneyTransfer(models.Model):
    user_name = models.CharField(max_length = 150, default = None)
    destination_account_number = models.IntegerField()
    transferred_amount = models.IntegerField()

def __str__(self):
        return self.user_name

class UserAccount(models.Model):
    account_number = models.IntegerField()
    balance = models.IntegerField()
    user_name = models.CharField(max_length = 150, default = None)

def __str__(self):
        return self.user_name