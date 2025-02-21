from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .models import *
from .forms import *
from django.http import HttpResponse
from django.conf import settings
import math,random
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404




# User Login
def user_login(req):
    if req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']

        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            # messages.success(req, "Login successful!")
            return redirect(home)  # Change 'home' to your actual homepage
        else:
            messages.error(req, "Invalid username or password!")

    return render(req, 'login.html')

# User Logout
def user_logout(req):
    logout(req)
    messages.success(req, "Logged out successfully!")
    return redirect('login')


def OTP(req):
    digits= "0123456789"
    OTP= ""
    for i in range(6):
        OTP += digits[math.floor(random.random()*10)]
    return OTP
# User Registration
def register(req):
    if req.method == "POST":
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']
        otp=OTP(req)

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(req, "Email is already registered!")
                return redirect(register)
            else:
                send_mail('Your OTP for Registaion',f"OTP for Registration {otp}",settings.EMAIL_HOST_USER,[email])
                messages.success(req,"Registration Successfull.Check OTP")
                return redirect("validate",name=username,password=password,email=email,otp=otp)
        else:
            messages.error(req, "Passwords do not match!")
    
    return render(req, 'register.html')

def validate(req,name,password,email,otp):
    if req.method=='POST':
        Otp=req.POST['Otp']
        if Otp==otp:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            messages.success(req,"OTP verified Successfully")
            return redirect(user_login)
        else:
            messages.error(req,"invalid Otp")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'validate.html',{'name':name,"pass":password,'emai':email,'otp':otp})

def home(req):
    return render(req,'home.html')

def add_doc(req):
    if req.method == 'POST':
        form = DocumentForm(req.POST, req.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = req.user  # Associate document with logged-in user
            document.save()
            return redirect(home)  # Redirect to a list of uploaded documents (create this view)
    else:
        form = DocumentForm()
    return render(req,'add_doc.html',{'form':form})

def add_img(req):
    if req.method == 'POST':
        form = ImageForm(req.POST, req.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = req.user  # Associate image with the logged-in user
            image.save()
            return redirect(home)  # Redirect to a list of uploaded images (you can create this view)
    else:
        form = ImageForm()
    return render(req,'add_img.html',{'form':form})
def add_message(req):
    if req.method =='POST':
        form=DiaryEntryForm(req.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.user=req.user
            message.save()
            return redirect(home)
    else:
        form=DiaryEntryForm()
    return render(req,'add_mes.html',{'form':form})

def document_list(req):
    documents = Document.objects.filter(user=req.user)
    
    for document in documents:
        if document.file.name.endswith('.pdf'):
            document.file_type = 'pdf'
        elif document.file.name.endswith('.doc') or document.file.name.endswith('.docx'):
            document.file_type = 'doc'
        else:
            document.file_type = 'other'
            
    return render(req, 'document_list.html', {'documents': documents})

def image_list(req):
    # Fetch all images uploaded by the logged-in user
    images = Image.objects.filter(user=req.user)
    return render(req, 'image_list.html', {'images': images})

def message_list(req):
    # Fetch all messages (diary entries) uploaded by the logged-in user
    messages = DiaryEntry.objects.filter(user=req.user)
    return render(req, 'message_list.html', {'messages': messages})

