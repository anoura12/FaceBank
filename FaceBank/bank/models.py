from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Face(models.Model):
    username = models.CharField(max_length=50)
    face = models.ImageField(upload_to='images/')

def __str__(self):
        return self.username

class MoneyTransfer(models.Model):
    enter_your_user_name = models.CharField(max_length = 150, default = None)
    enter_the_destination_account_number = models.IntegerField()
    enter_the_amount_to_be_transferred_in_INR = models.IntegerField()

class Status (models.Model):
    account_number = models.IntegerField()
    balance = models.IntegerField()
    user_name = models.CharField(max_length = 150, default = None)