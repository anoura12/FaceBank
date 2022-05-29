from django.shortcuts import render,redirect
import requests
import random
from django.http import HttpResponseServerError,StreamingHttpResponse
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
from urllib.parse import urlparse
from io import BytesIO
# To install this module, run:
# python -m pip install Pillow
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, QualityForRecognition


# ======================================================================


# This key will serve all examples in this document.
KEY = 'bb38949700fc42ada84a3ef4e4610e69'

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = 'https://anoushkafaceapi.cognitiveservices.azure.com/'

def index(request):
    return render(request, 'main/index.html')

def face_capture(request):
    context = dict()
    print(request.POST)
    if request.method == 'POST':
        username = 'anoushka'
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
        return redirect('/')
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
        
            curr_user = MoneyTransfer.objects.get(enter_your_user_name=request.user)
            dest_user_acc_num = curr_user.enter_the_destination_account_number

            temp = curr_user # Delete this instance once money transfer is done
            
            dest_user = UserAccount.objects.get(account_number=dest_user_acc_num) # FIELD 1
            transfer_amount = curr_user.enter_the_amount_to_be_transferred_in_INR # FIELD 2
            curr_user = UserAccount.objects.get(user_name=request.user) # FIELD 3

            # Now transfer the money!
            curr_user.balance = curr_user.balance - transfer_amount
            dest_user.balance = dest_user.balance + transfer_amount

            # Save the changes before redirecting
            curr_user.save()
            dest_user.save()

            temp.delete() 
            return redirect("main/profile.html")
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

        face = Face.objects.all().values('face')
        print(face[0]['face'])
        face_src_image = 'media/' + face[0]['face']

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


        for matched_face in matched_faces:
            for face in response_detected_faces:
                if face.face_id == matched_face.face_id:
                    print(face.face_id)
                    print(matched_face.face_id)
                    print('Face Matched!')
                if (face.face_id != matched_face.face_id):
                    print('Face not matched!')
        
        default_storage.delete(tmp_file)
    return render(request,'main/face_verify.html')
    

def dashboard(request):
    return render(request, 'main/dashboard.html')




# Base url for the Verify and Facelist/Large Facelist operations
IMAGE_BASE_URL = 'https://algorithmwatch.org/en/wp-content/uploads/2021/03/Team-Mosaic-New-Faces-March-2021.jpg'


face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

import os
import io
import json
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont

"""
Example 4. Detect if a face shows up in other photos/images
"""




   