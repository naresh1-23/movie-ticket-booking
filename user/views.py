from django.shortcuts import render, redirect
from .models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password

# Create your views here.
def loginView(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST["username"]
        password= request.POST["password"]
        if username == "" or password == "":
            messages.warning(request, "Fields cannot be empty")
            return redirect("login")
        user = authenticate(username= username, password = password)
        if user:
            login(request, user)
            messages.success(request, "Successfully logged in")
            if user.is_superuser:
                return redirect("now-showing")
            return redirect("home")
        messages.warning(request, "User doesn't exists")
        return redirect("login")
    return render(request, "user/login.html")


def registerView(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        password= request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if username == "" or firstname == "" or lastname == '' or email == "" or mobile == "" or password == "" or confirm_password =="":
            messages.warning(request, "Fields cannot be empty")
            return redirect("register")
        elif password != confirm_password:
            messages.warning(request, "password didn't matched")
            return redirect("register")
        elif not mobile.isdigit() or len(mobile) != 10:
            messages.warning(request, "Invalid number")
            return redirect("register")
        else:
            user1 = User.objects.filter(Q(username = username) | Q(email = email))
            if user1:
                messages.warning(request, "Username already exists")
                return redirect("register")
            user = User.objects.create(username = username, email = email , first_name = firstname, last_name = lastname, mobile_number = mobile, password = make_password(password))
            user.save()
            messages.success(request, "Account successfully created")
            return redirect('login')
    return render(request, "user/signup.html")


def logoutView(request):
    logout(request)
    messages.success(request, "Successfullt logged out")
    return redirect("home")