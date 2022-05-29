from django.shortcuts import render,redirect
import requests
import random
from django.http import HttpResponse
from django.views.decorators import gzip
import threading
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
# Create your views here.
from bank.models import Face, MoneyTransfer, UserAccount
import sys
from urllib.request import urlopen

from bank.forms import MoneyTransferForm

from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
import base64

import asyncio
from email.mime import image
import io
import glob
import os
import sys
import time
from tkinter import Frame
import uuid
import requests

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition
from django.contrib.auth import authenticate, login, logout
from dotenv import load_dotenv

# ======================================================================

load_dotenv()
# This key will serve all examples in this document.
KEY = os.getenv('KEY')

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = os.getenv('ENDPOINT')

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def index(request):
    return render(request, 'main/index.html')
    

def face_capture(request):
    context = dict()
    username = None
    if request.method == 'POST':
        username = request.user.username
        image_path = request.POST["src"]# src is the name of input attribute in your html file, this src value is set in javascript code
        format, imgstr = image_path.split(';base64,') 
        ext = format.split('/')[-1] 

        image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        
        if image is not None:
            obj = Face.objects.create(username=username, face=image)  # create a object of Image type defined in your model
            obj.save()
            context["path"] = obj.face.url  #url to image stored in my server/local device
            context["username"] = obj.username
        else :
            return redirect('/')
        return redirect('main:dashboard')
    return render(request, 'main/face_capture.html', context=context)

def randomGen():
    # returns a 6 digit random number
    return int(random.uniform(100000, 999999))

def create_bank_account(request):
    try:
        curr_user = UserAccount.objects.get(user_name=request.user) # getting details of current user
    except:
        # if no details exist (new user), create new details
        curr_user = UserAccount()
        curr_user.account_number = randomGen() # random account number for every new user
        curr_user.balance = 0
        curr_user.user_name = request.user
        curr_user.save()
    return render(request, "main/profile.html", {"curr_user": curr_user})
    
def money_transfer(request):
     if request.method == "POST":
        form = MoneyTransferForm(request.POST)
        if form.is_valid():
            form.save()

            print(request.user)
            print(request.user.username)
            curr_user = MoneyTransfer.objects.get(user_name=request.user.username)
            dest_user_acc_num = curr_user.destination_account_number

            temp = curr_user # Delete this instance once money transfer is done
            
            dest_user = UserAccount.objects.get(account_number=dest_user_acc_num) # FIELD 1
            transfer_amount = curr_user.transferred_amount # FIELD 2
            curr_user = UserAccount.objects.get(user_name=request.user.username) # FIELD 3

            # Now transfer the money!
            curr_user.balance = curr_user.balance - transfer_amount
            dest_user.balance = dest_user.balance + transfer_amount

            # Save the changes before redirecting
            curr_user.save()
            dest_user.save()

            temp.delete() 
            return render(request, "main/bank_account_details.html", {"curr_user": curr_user})
     else:
        form = MoneyTransferForm()
        return render(request, "main/money_transfer.html", {"form": form})

def face_verify(request):
    context = dict()
    if request.method == 'POST':
        image_path = request.POST["src"]# src is the name of input attribute in your html file, this src value is set in javascript code
        format, imgstr = image_path.split(';base64,') 
        ext = format.split('/')[-1] 

        imageFile = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        path = default_storage.save('tmp/somename.png', imageFile)
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        print(imageFile)
        print(tmp_file)

        faces = Face.objects.all()
        f = ''
        for face in faces:
            if request.user.username == face.username:
                f = face.face
                print(f)
        face_src_image = 'media/' + str(f)

        response_detected_faces = face_client.face.detect_with_stream(
        image=open(tmp_file, 'rb'),
        detection_model='detection_03',
        recognition_model='recognition_04',  
        )
        face_ids = [face.face_id for face in response_detected_faces]
        # print(face_ids)

        img_source = open(face_src_image, 'rb')
        response_face_source = face_client.face.detect_with_stream(
            image=img_source,
            detection_model='detection_03',
            recognition_model='recognition_04'    
        )
        face_id_source = response_face_source[0].face_id
        # print(face_id_source)

        matched_faces = face_client.face.find_similar(
            face_id=face_id_source,
            face_ids=face_ids
        )

        print(matched_faces)

        if len(matched_faces) == 0:
            print('Face not matched')
            default_storage.delete(tmp_file)
            return render(request, 'main/404.html')



        for matched_face in matched_faces:
            for face in response_detected_faces:
                if face.face_id == matched_face.face_id:
                    print('Face Matched!')
                    default_storage.delete(tmp_file)
                    return redirect('main:money_transfer')
        
        default_storage.delete(tmp_file)
    return render(request,'main/face_verify.html')
    

def dashboard(request):
    return render(request, 'main/dashboard.html')

def bank_account_details(request):
    curr_user = UserAccount.objects.get(user_name=request.user) 
    return render(request, 'main/bank_account_details.html',{"curr_user": curr_user})













   