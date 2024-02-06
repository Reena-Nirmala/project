# # myapp/views.py
# from django.core.mail import send_mail
# from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password, check_password
# from django.utils.crypto import get_random_string
#
# from .models import User
# from django.contrib.auth import get_user_model
#
# from django.conf import settings
#
# User = get_user_model()
#
#
# def signup(request):
#     if request.method == 'POST':
#         email = request.POST.get('email', '')
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         confirm_password = request.POST.get('confirm_password', '')
#
#         if not (username and password and confirm_password):
#             # Handle missing fields error
#             error_message = "Username, password, and confirm password are required."
#             return render(request, 'signup.html', {'error_message': error_message})
#
#         if len(password) < 8:
#             error_message = "Password must be at least 8 characters long."
#             return render(request, 'signup.html', {'error_message': error_message})
#
#         if password != confirm_password:
#             error_message = "Passwords do not match."
#             return render(request, 'signup.html', {'error_message': error_message})
#
#         hashed_password = make_password(password)
#         User.objects.create(
#             email=email,
#             username=username,
#             password=hashed_password
#         )
#         return redirect('login')
#
#     return render(request, 'signup.html')
#
#
# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#
#         user = User.objects.filter(username=username).first()
#         if user and check_password(password, user.password):
#             # Set user as logged in
#             return redirect('index')
#         else:
#             error_message = "Invalid username or password."
#             return render(request, 'login.html', {'error_message': error_message})
#
#     return render(request, 'login.html')
#
#
# def logout(request):
#     return render(request, 'home.html')
#
#
# def home(request):
#     return render(request, 'home.html')
#
#
# def dashboard(request):
#     return render(request, 'dashboard.html')
# def profile(request):
#     return render(request,'profile.html')
#
# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email', '')
#         user = User.objects.filter(email=email).first()
#
#         if user:
#             # Generate a unique token and save it to the user model
#             token = get_random_string(length=32)
#             user.reset_password_token = token
#             user.save()
#
#             # Send the password reset email with the token
#             reset_link = f"http://127.0.0.1:8000/SummarEase/reset_password/{token}/"
#
#             send_mail(
#                 'Reset Password',
#                 f'Click the following link to reset your password: {reset_link}',
#                 settings.DEFAULT_FROM_EMAIL,
#                 [user.email],
#                 fail_silently=False,
#             )
#             return render(request, 'forgot_password_success.html')
#
#         else:
#             error_message = "No user found with this email address."
#             return render(request, 'forgot_password.html', {'error_message': error_message})
#
#     return render(request, 'forgot_password.html')
#
#
# def reset_password(request, token):
#     user = User.objects.filter(reset_password_token=token).first()
#
#     if not user:
#         # Handle invalid or expired token
#         return render(request, 'invalid_token.html')
#
#     if request.method == 'POST':
#         new_password = request.POST.get('new_password', '')
#         confirm_new_password = request.POST.get('confirm_new_password', '')
#
#         if new_password != confirm_new_password:
#             error_message = "Passwords do not match."
#             return render(request, 'reset_password.html', {'error_message': error_message, 'token': token})
#
#         # Update the user's password and reset the token
#         user.password = make_password(new_password)
#         user.reset_password_token = None
#         user.save()
#
#         return redirect('reset_password_confirm')
#
#     return render(request, 'reset_password.html', {'token': token})
#
#
# def reset_password_confirm(request):
#     return render(request, 'reset_password_confirm.html')


# myapp/views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from django.utils.crypto import get_random_string

from .models import User
from django.contrib.auth import get_user_model

from django.conf import settings
import re

user = get_user_model()

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        print(email, username, password)

        if not (username and password and confirm_password):
            # Handle missing fields error
            error_message = "Username, password, and confirm password are required."
            return render(request, 'signup.html', {'error_message': error_message})



        if not (re.match(r'^(?=.*[a-zA-Z])[a-zA-Z0-9_]{8,}$', password)):
            error_message = "Password should be alphanumeric, at least 8 characters long, and contain at least one alphabetic character."
            return render(request, 'signup.html', {'error_message': error_message})

        if len(password) < 8:
            error_message = "Password must be at least 8 characters long."
            return render(request, 'signup.html', {'error_message': error_message})

        if password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, 'signup.html', {'error_message': error_message})

        try:
            hashed_password = make_password(password)
            User.objects.create(
                email=email,
                username=username,
                password=hashed_password
            )
            success_message = "Registration successful..!!"
            login_url = reverse('login')
            redirect_url = f'{login_url}?success_message={success_message}'
            return redirect(redirect_url)

        except Exception as e:
            error_message = "User already exists."
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')


def login(request):
    success_message = request.GET.get('success_message', '')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = User.objects.filter(username=username).first()
        if user and check_password(password, user.password):
            # Set user as logged in
            print(user.id)
            request.session['user_id'] = user.id
            return redirect('index')
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html',{'success_message': success_message})


def logout(request):
    # Your logout logic here
    return render(request, 'home.html')


def home(request):
    return render(request, 'home.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def profile(request):
    return render(request, 'profile.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate a unique token and save it to the user model
            token = get_random_string(length=32)
            user.reset_password_token = token
            user.save()

            # Send the password reset email with the token
            reset_link = f"http://127.0.0.1:8000/SummarEase/reset_password/{token}/"

            send_mail(
                'Reset Password',
                f'Click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return render(request, 'forgot_password_success.html')

        else:
            error_message = "No user found with this email address."
            return render(request, 'forgot_password.html', {'error_message': error_message})

    return render(request, 'forgot_password.html')


def reset_password(request, token):
    user = User.objects.filter(reset_password_token=token).first()

    if not user:
        # Handle invalid or expired token
        return render(request, 'invalid_token.html')

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_new_password = request.POST.get('confirm_new_password', '')

        if new_password != confirm_new_password:
            error_message = "Passwords do not match."
            return render(request, 'reset_password.html', {'error_message': error_message, 'token': token})

        # Update the user's password and reset the token
        else:
            user.set_password(new_password)
            user.reset_password_token = None
            user.save()

            return redirect('reset_password_confirm')

    return render(request, 'reset_password.html', {'token': token})


def reset_password_confirm(request):
    return render(request, 'reset_password_confirm.html')
