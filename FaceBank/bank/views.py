from django.shortcuts import render,redirect
from django.core.files.storage import default_storage
from django.conf import settings

from bank.models import Face, MoneyTransfer, UserAccount
from bank.forms import MoneyTransferForm

from django.core.files.base import ContentFile
import base64

import os
import requests
import random

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv

# ======================================================================

load_dotenv() # to load environment variables

KEY = os.getenv('KEY') # This key will serve all examples in this document.

ENDPOINT = os.getenv('ENDPOINT')  # This endpoint will be used in all examples in this quickstart.

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def index(request):
    '''
    Landing Page for app
    '''

    return render(request, 'main/index.html')
    

def face_capture(request):
    '''
    To register the face in the database
    '''
    context = dict()
    username = None
    if request.method == 'POST':
        username = request.user.username
        image_path = request.POST["src"]# src is the name of input attribute in html file, this src value is set in javascript code
        format, imgstr = image_path.split(';base64,') 
        ext = format.split('/')[-1] 

        image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        
        if image is not None:
            obj = Face.objects.create(username=username, face=image)  # create a object of Face type defined in your model
            obj.save()
            context["path"] = obj.face.url  # url to image stored in my server/local device
            context["username"] = obj.username
        else :
            return redirect('/')
        return redirect('main:dashboard')
    return render(request, 'main/face_capture.html', context=context)

def randomGen():
    '''
    returns a 6 digit random number
    '''
    return int(random.uniform(100000, 999999))

def create_bank_account(request):
    '''
    creates a bank account for user using the randomly generated 5 digit number
    '''
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
     '''
     transacts money from source account number to destination account number
     '''
     if request.method == "POST":
        form = MoneyTransferForm(request.POST)
        if form.is_valid():
            form.save()

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
    '''
    verifies the face captured against the registered face in the database using Azure Face API
    '''
    if request.method == 'POST':
        image_path = request.POST["src"] # src is the name of input attribute in html file, this src value is set in javascript code
        format, imgstr = image_path.split(';base64,') 
        ext = format.split('/')[-1] 

        imageFile = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # converts the base 64 url into a file that is the destination img

        path = default_storage.save('tmp/somename.png', imageFile)
        tmp_file = os.path.join(settings.MEDIA_ROOT, path) # saves the destination img as a temp file which will be deleted later

        faces = Face.objects.all()
        f = ''
        for face in faces:
            if request.user.username == face.username:
                f = face.face #extracts each face

        face_src_image = 'media/' + str(f)

        response_detected_faces = face_client.face.detect_with_stream( #detects face in destination img
        image=open(tmp_file, 'rb'),
        detection_model='detection_03',
        recognition_model='recognition_04',  
        )
        face_ids = [face.face_id for face in response_detected_faces]

        img_source = open(face_src_image, 'rb')
        response_face_source = face_client.face.detect_with_stream( # detects face in source img (img in database)
            image=img_source,
            detection_model='detection_03',
            recognition_model='recognition_04'    
        )
        face_id_source = response_face_source[0].face_id

        matched_faces = face_client.face.find_similar( # checks whether face_source and face_dest have same face ids
            face_id=face_id_source,
            face_ids=face_ids
        )


        if len(matched_faces) == 0: # case where faces do not match
            print('Face not matched')
            default_storage.delete(tmp_file)
            return render(request, 'main/404.html')



        for matched_face in matched_faces:
            for face in response_detected_faces:
                if face.face_id == matched_face.face_id: # case where face matches
                    print('Face Matched!')
                    default_storage.delete(tmp_file)
                    return redirect('main:money_transfer')
        
        default_storage.delete(tmp_file)
    return render(request,'main/face_verify.html')
    

def dashboard(request):
    '''
    Dashboard of the app
    '''
    return render(request, 'main/dashboard.html')

def bank_account_details(request):
    '''
    Allows user to view their bank account details
    '''
    curr_user = UserAccount.objects.get(user_name=request.user) 
    return render(request, 'main/bank_account_details.html',{"curr_user": curr_user})













   