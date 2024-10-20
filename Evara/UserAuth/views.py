from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import OTP
import random
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from datetime import timedelta

def generate_otp():
    return random.randint(100000, 999999)

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    send_mail(subject, message, 'your_email@gmail.com', [email])

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already taken."
            return render(request, 'register.html', {'error_message': error_message})

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            error_message = "Email already registered."
            return render(request, 'register.html', {'error_message': error_message})

        # Check if passwords match
        if password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, 'register.html', {'error_message': error_message})

        # Generate OTP
        otp = generate_otp()
        expires_at = timezone.now() + timedelta(minutes=5)

        # Store OTP in the database
        OTP.objects.create(email=email, otp=otp, expires_at=expires_at)

        # Send OTP to email
        send_otp_email(email, otp)

        # Store user information in session
        request.session['username'] = username
        request.session['first_name'] = first_name
        request.session['last_name'] = last_name
        request.session['password'] = password

        # Redirect to OTP verification page
        return redirect('verify_otp', email=email)

    return render(request, 'register.html')


def verify_otp(request, email):
    if request.method == 'POST':
        entered_otp = request.POST['otp']

        # Retrieve OTP from the database
        try:
            otp_instance = OTP.objects.get(email=email)
        except OTP.DoesNotExist:
            error_message = "OTP not found. Please register again."
            return render(request, 'otp.html', {'error_message': error_message})

        # Check if the entered OTP matches
        if entered_otp == str(otp_instance.otp) and not otp_instance.is_expired():
            # OTP is correct and valid, now register the user
            try:
                username = request.session['username']
                first_name = request.session['first_name']
                last_name = request.session['last_name']
                password = request.session['password']
            except KeyError:
                error_message = "Session data missing. Please register again."
                return redirect('register')

            # Create a new user
            User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

            # Clear session data
            request.session.flush()

            return redirect('login')  # Redirect to login page after successful registration
        else:
            error_message = "Invalid OTP or OTP expired."
            return render(request, 'otp.html', {'error_message': error_message})

    return render(request, 'otp.html', {'email': email})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        
        user = authenticate(request,username = username,password = pass1)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return render(request,'login.html',{'error':'Username or Password is Wrong'})
    return render(request,'login.html')


def user_logout(request):
    print("kasjkll;jksadf")
    logout(request)
    return redirect('index')