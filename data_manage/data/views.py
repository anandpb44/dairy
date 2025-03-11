from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .models import *
from .forms import *
from django.http import HttpResponse
from django.conf import settings
import math,random
import os
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404


def user_login(req):
    if req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']

        user = authenticate(req, username=username, password=password)

        if user is not None:
            # Generate and store OTP
            otp = generate_otp()
            req.session['otp'] = otp
            req.session['login_user'] = username  # Store username in session

            # Send OTP via email
            send_mail(
                'Your OTP for Login',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [user.email]
            )

            messages.success(req, "An OTP has been sent to your email. Please verify to continue.")
            return redirect(otp_login)

        else:
            messages.error(req, "Invalid username or password!")

    return render(req, 'login.html')



def generate_otp():
    return ''.join(random.choices("0123456789", k=6))

def otp_login(req):
    if req.method == "POST":
        entered_otp = req.POST['otp']
        stored_otp = req.session.get('otp')
        username = req.session.get('login_user')

        if not stored_otp or not username:
            messages.error(req, "Session expired! Please log in again.")
            return redirect(user_login)

        if entered_otp == stored_otp:
            user = User.objects.get(username=username)
            login(req, user)  # Log the user in

            # Clear session data
            del req.session['otp']
            del req.session['login_user']

            messages.success(req, "Login successful!")
            return redirect(home)

        else:
            messages.error(req, "Invalid OTP! Please try again.")
            return redirect(otp_login)

    return render(req, 'otp_login.html')


# def user_login(req):
#     if req.method == "POST":
#         username = req.POST['username']
#         password = req.POST['password']

#         user = authenticate(req, username=username, password=password)
#         if user is not None:
#             req.session['user']=username
#             login(req, user)
           
#             return redirect(home)
#         else:
#             messages.error(req, "Invalid username or password!")

#     return render(req, 'login.html')



def validate_login(req):
    if req.method == "POST":
        entered_otp = req.POST['otp']
        stored_otp = req.session.get('otp')
        pending_user = req.session.get('pending_user')

        if not stored_otp or not pending_user:
            messages.error(req, "Session expired! Please register again.")
            return redirect(register)

        if entered_otp == stored_otp:
            # Create and log in the user
            user = User.objects.create_user(
                username=pending_user['email'],  
                first_name=pending_user['username'],
                email=pending_user['email'],
                password=pending_user['password']
            )
            user.save()

            # Log the user in
            user = authenticate(req, username=pending_user['email'], password=pending_user['password'])
            if user:
                login(req, user)
                messages.success(req, "Login successful!")
                
                # Clear session data
                del req.session['pending_user']
                del req.session['otp']

                return redirect(home)

        else:
            messages.error(req, "Invalid OTP! Please try again.")
            return redirect(validate_login)

    return render(req, 'validate_login.html')




def user_logout(req):
    logout(req)
    messages.success(req, "Logged out successfully!")
    return redirect(user_login)


def OTP(req):
    digits= "0123456789"
    OTP= ""
    for i in range(6):
        OTP += digits[math.floor(random.random()*10)]
    return OTP
# User Registration
# def register(req):
#     if req.method == "POST":
#         username = req.POST['username']
#         email = req.POST['email']
#         password = req.POST['password']
#         confirm_password = req.POST['confirm_password']
#         otp=OTP(req)

#         if password == confirm_password:
#             if User.objects.filter(email=email).exists():
#                 messages.error(req, "Email is already registered!")
#                 return redirect(register)
#             else:
#                 send_mail('Your OTP for Registaion',f"OTP for Registration {otp}",settings.EMAIL_HOST_USER,[email])
#                 messages.success(req,"Registration Successfull.Check OTP")
#                 return redirect("validate",name=username,password=password,email=email,otp=otp)
#         else:
#             messages.error(req, "Passwords do not match!")
    
#     return render(req, 'register.html')
def register(req):
    if req.method == "POST":
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        confirm_password = req.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(req, "Passwords do not match!")
            return redirect(register)

        if User.objects.filter(email=email).exists():
            messages.error(req, "Email is already registered!")
            return redirect(register)

        # Generate OTP
        otp = generate_otp()

        # Store user data in session temporarily
        req.session['pending_user'] = {'username': username, 'email': email, 'password': password}
        req.session['otp'] = otp

        # Send OTP via email
        send_mail(
            'Your OTP for Login Verification',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email]
        )

        messages.success(req, "Registration successful! Check your email for the OTP.")
        return redirect("validate",name=username,password=password,email=email,otp=otp)

    return render(req, 'register.html')

def validate(req,name,password,email,otp):
    if req.method=='POST':
        Otp=req.POST['Otp']
        if Otp==otp:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            messages.success(req,"OTP verified Successfully")
            return redirect('user_login')
        else:
            messages.error(req,"invalid Otp")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'validate.html',{'name':name,"pass":password,'emai':email,'otp':otp})



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


def home(req):
    img=Image.objects.all()
    documents = Document.objects.filter(user=req.user)[::-1]
    
    for document in documents:
        if document.file.name.endswith('.pdf'):
            document.file_type = 'pdf'
        elif document.file.name.endswith('.doc') :
            document.file_type = 'doc'
        elif document.file.name.endswith('.docx'):
            document.file_type='docx'
        else:
            document.file_type = 'other'

    return render(req,'home.html',{'documents': documents,'data1':img}) 

def document_list(req):
    documents = Document.objects.filter(user=req.user)[::-1]
    
    for document in documents:
        if document.file.name.endswith('.pdf'):
            document.file_type = 'pdf'
        elif document.file.name.endswith('.doc') :
            document.file_type = 'doc'
        elif document.file.name.endswith('.docx'):
            document.file_type='docx'
        else:
            document.file_type = 'other'
            
    return render(req, 'document_list.html', {'documents': documents})

def image_list(req):
    # Fetch all images uploaded by the logged-in user
    images = Image.objects.filter(user=req.user)[::-1]
    
    return render(req, 'image_list.html', {'images': images})

def message_list(req):
    # Fetch all messages (diary entries) uploaded by the logged-in user
    messages = DiaryEntry.objects.filter(user=req.user)
    return render(req, 'message_list.html', {'messages': messages})


def mess_delete(req,mid):
    data=DiaryEntry.objects.get(pk=mid)
    data.delete()
    return redirect(message_list)


def doc_delete(req,id):
    data=Document.objects.get(pk=id)
    data.delete()
    return redirect(document_list)


def img_delete(req,img_id):
    data=Image.objects.get(pk=img_id)
    file=data.image.path
    os.remove(file)
    data.delete()
    return redirect(image_list)