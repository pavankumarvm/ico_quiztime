import random
import http
from datetime import datetime, timezone

from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy,reverse
from django.core.mail import send_mail
from django.contrib import messages

from .serializers import IcoUserSerializer
from .models import IcoUser,Otp

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        usertype = request.POST.get('usertype')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if usertype == None or usertype == "":
            usertype = 'S'

        if not (first_name and last_name and email and password1 and password2):
            messages.error(request, 'Fill the Empty Fields.')
            return render(request,
                          template_name='register.html')
        elif password1 == password2:
            if IcoUser.objects.filter(username=username):
                messages.error(
                    request, 'Username already exists.Try another.')
                return render(request, 'register.html')
            elif IcoUser.objects.filter(email=email):
                messages.error(
                    request, 'Email Address already exists.Try another.')
                return render(request, 'register.html')
            else:
                user = IcoUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name,
                    usertype=usertype)
                messages.success(request, 'User registered successfully.')
                return redirect("/bajajauto/user/dashboard/")
        else:
            messages.error(request, "Passwords doesn't match")
            return render(request, 'register.html')
    else:
        return render(request,
                      template_name='register.html')

def new_admin(request):
    if request.method == 'POST':
        usertype = request.POST.get('usertype')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')

        if not (username and email and password):
            messages.error(request, 'Fill the Empty Fields.')
            return render(request, template_name='new_admin.html')
        else:
            if IcoUser.objects.filter(username=username):
                messages.error(
                    request, 'Username already exists.Try another.')
                return render(request, 'new_admin.html')
            elif IcoUser.objects.filter(email=email):
                messages.error(
                    request, 'Email Address already exists.Try another.')
                return render(request, template_name='new_admin.html')
            else:
                user = IcoUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name="Admin",
                    last_name="",
                    usertype=usertype)
                messages.success(request, 'User registered successfully.')
                return redirect("/bajajauto/adminpanel/dashboard/")
    else:
        return render(request,
                      template_name='new_admin.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            if user.is_admin and login_type == 'admin':
                return redirect('/bajajauto/adminpanel/dashboard/')
            else:
                return redirect('/bajajauto/user/dashboard/')
        else:
            messages.error(request, 'Wrong username or password.')
            return render(request,
                    template_name='login.html',
                )
    else:
        return render(request,
                    template_name='login.html',
                )

def login_admin(request):
    if request.method == 'GET':
        return render(
            request,
            template_name='adminlogin.html',
        )


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/')


def random_otp():
    random_str = ""
    for i in range(6):
        if i==0:
            random_str += str(random.randrange(1,9,1))
        else:
            random_str += str(random.randrange(0,9,1))
    return random_str


def forgot_password(request):
    if request.method == 'POST':
        data = {}
        email = request.POST.get('email')
        if IcoUser.objects.filter(email=email):
            user = IcoUser.objects.get(email=email)
            if Otp.objects.filter(user=user):
                otp_obj = Otp.objects.get(user=user)
                if (datetime.now(timezone.utc) - otp_obj.otp_valid_time).total_seconds() < 120 and otp_obj.no_of_attempts == 0:
                    messages.error(request, 'Please try after 30 minutes')
                    Otp.objects.filter(user=user).delete()
            else:
                random_str = random_otp()
                otp_obj = Otp(user=user, otp=random_str)
                otp_obj.save()

                messages.success(request, 'OTP generated successfully')

                mail_message = "You're receiving this email because you requested a password reset\nfor your user account at EduAccess.\n\n\tOTP is : "
                mail_message += random_str
                mail_message += "\n\nYour username, in case you've forgotten: " + user.username
                mail_message += "\n\n\tThanks for using our site!\n"
                
                send_mail(
                    'Password Reset',
                    mail_message,
                    'noreply@eduacess.in',
                    [
                        email,
                    ]
                )
                return redirect(reverse('reset-password'))
        else:
            messages.error(request,'No user registered with : '+ email)
        return render(request, 'forgot_password.html')
    else:
        return render(request, 'forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        data = {}
        email = request.POST.get('email')
        OTP = request.POST.get('OTP')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, "Password doesn't match")
            return render(request, 'reset_password.html', data)
        if IcoUser.objects.filter(email=email):
            user = IcoUser.objects.get(email=email)
            if Otp.objects.filter(user=user):
                otp_obj = Otp.objects.get(user=user)
                if otp_obj.no_of_attempts == 0:
                    messages.error(request, 'No. of attempts exceeded limit.')
                    return render(request, 'reset_password.html', data)
                if otp_obj.otp != OTP:
                    messages.error(request, 'OTP is incorrect.')
                    return render(request, 'reset_password.html', data)
                user.set_password(new_password)
                user.save()
                otp_obj.delete()
                messages.success(request, 'Password Changed Succesfully.')
                return redirect('/bajajauto/accounts/login')
            else:
                messages.error(request, 'OTP expired. Regenrate OTP.')
                return render(request, 'forgot_password.html', data)
        else:
            messages.error(request, 'email is incorrect.')
        return render(request, 'reset_password.html', data)
    else:
        return render(request, 'reset_password.html')

def update_details(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        files = request.FILES.getlist('image')
        avatar = None
        if len(files) != 0:
            avatar = files[0]

        if not (first_name and last_name and email):
            messages.error(request, 'Fill the Empty Fields.')
            return render(request,
                          template_name='profile.html')
        else:
            user = IcoUser.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.phone_no = phone_no
            user.age = age
            user.gender = gender
            if avatar:
                user.avatar = avatar
            messages.success(request, 'User Details updated successfully.')
            return redirect("/admin_panel/dashboard/")
    else:
        return render(request,
                      template_name='profile.html')


def change_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = authenticate(email=email, password=password)
        if user is not None:
            if password1 == password2:
                print(password1)
                user.set_password(password1)
                user.save()
                messages.success(
                    request, "Password updated Successfully.Login Again.")
                return render(request, template_name='login.html')
            else:
                messages.error(request, "Passwords doesn't match")
                return render(request, 'change_password.html')
        else:
            messages.error(request, 'Wrong Current Password.')

            return render(request,
                          template_name='change_password.html',
                          )
    else:
        return render(request,
                      template_name='change_password.html',
                      )