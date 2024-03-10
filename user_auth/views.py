from django.shortcuts import render, redirect
from .models import MyUser
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def login_user(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        email = request.POST.get("email")
        user = None
        try:
            user = MyUser.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")
            return redirect("user_auth:login_user")
        if user.email != email:
            messages.error(request, "Email Does not match.")
            return redirect("user_auth:login_user")

        user = authenticate(request, username=username, password=password, email=email)
        if user is not None:
            login(request, user)
            return redirect("index:home")
        else:
            messages.error(request, "Invalid password.")

    return render(request, "user_auth/login.html")


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_already_exists = False
        try:
            already_user = MyUser.objects.get(username=username)
        except:
            user_already_exists = True
        if not user_already_exists:
            messages.error(request, "Username already exists.")
            return redirect("user_auth:register_user")

        email_already_exists = False
        try:
            already_email = MyUser.objects.get(email=email)
        except:
            email_already_exists = True
        if not email_already_exists:
            messages.error(request, "Email already exists.")
            return redirect("user_auth:register_user")

        if password == confirm_password:

            user = MyUser.objects.create_user(username=username, email=email, password=password)

            login(request, user)

            return redirect('index:home')
        else:
            messages.error(request, "Passwords do not match.")
            return redirect("user_auth:register_user")

    return render(request, "user_auth/register.html")


def logout_user(request):
    print(request)
    logout(request)
    return redirect("index:home")
