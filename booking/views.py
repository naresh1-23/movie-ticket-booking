from django.shortcuts import render, redirect
from admin_page.models import Movie, NowShowing, ShowTime, Booked
from user.models import User
from datetime import datetime, timedelta
from django.db.models import Count
import json
from django.http import HttpResponse
from django.contrib import messages
from django.core.serializers import serialize
from django.contrib.auth.hashers import make_password, check_password



def home(request):
    delete_movie = NowShowing.objects.filter(running_date__lt = datetime.now().date())
    delete_movie.delete()
    delete_showtime = ShowTime.objects.filter(date__lt = datetime.now().date())
    delete_showtime.delete()
    movies = Movie.objects.filter(releasing_date__gt = datetime.now().date())
    now_showing_movies = NowShowing.objects.filter(running_date=datetime.now().date())
    current_time = datetime.now().time()
    tom = False
    return render(request, "booking/home.html", {"movies": movies, "now_showing_movies": now_showing_movies, "tom": tom, "current_time": current_time})


def upcoming_movie(request, pk):
    movie = Movie.objects.filter(id = pk).first()
    return render(request, "booking/upcoming_movie.html", {"movie": movie})

def tomorrow(request):
    tomorrow = datetime.now().date() + timedelta(days=1)
    movies = Movie.objects.filter(releasing_date__gt = datetime.now().date())
    now_showing_movies = NowShowing.objects.filter(running_date=tomorrow)
    tom = True
    return render(request, "booking/home.html", {"now_showing_movies": now_showing_movies, "movies": movies, "tom": tom})


def seat_booking(request, pk, tom, showtime):
    movie = Movie.objects.filter(id = pk).first()
    showtime_obj = ShowTime.objects.filter(time = showtime).first()
    current_time = datetime.now().time()
    if tom == 'True':
        tomorrow = datetime.now().date() + timedelta(days=1)
        now_showing_movies = NowShowing.objects.filter(running_date=tomorrow, movie=movie).first()

        tomm = True
    else:
        now_showing_movies = NowShowing.objects.filter(running_date=datetime.now().date(), movie = movie).first()
        tomm = False 
    if request.method == "POST":
        seats_input = request.POST["seat"]
        seats = []
        seats = seats_input.split(",")
        for seat in seats:
            book = Booked.objects.create(user = request.user, show=now_showing_movies, time=showtime_obj, seat = seat)
            book.save()
        messages.success(request, "Seat successfully booked")
        return redirect("home")
    booked_seats = serialize('json',Booked.objects.filter(show = now_showing_movies, time=showtime_obj))
    seat_range = [1,2,3,4,5,6,7,8]
    return render(request,"booking/seat_booking.html", {"current_time":current_time,'movie': movie, "now_showing_movies": now_showing_movies,"tomm": tomm, "seat_range": seat_range , "showtime_obj": showtime_obj.time, "booked_seats": booked_seats})


def profile(request, pk):
    user = User.objects.filter(id = pk).first()
    booked = Booked.objects.filter(user = user)
    return render(request, "booking/profile.html", {"user": user, "booked": booked})

def editProfile(request, pk):
    user = User.objects.filter(id = pk).first()
    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        mobile_number =request.POST["mobile"]
        username = request.POST["username"]
        email = request.POST["email"]
        if first_name == "" or last_name == '' or email == "" or mobile_number == "" or username == "":
            messages.warning(request, "Fields cannot be empty")
            return redirect("editprofile", pk = pk)
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.mobile_number = mobile_number
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Data successfully changed")
            return redirect("profile", pk = pk)
    return render(request, "booking/edit_profile.html")


def changePassword(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            old_password = request.POST["old_password"]
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if old_password == "" or new_password == "" or confirm_password == "":
                messages.warning(request, "Fields cannot be empty")
                return redirect("change-password")
            elif not check_password(old_password, user.password):
                messages.warning(request, "Old Password didn't matched")
                return redirect("change-password")
            elif new_password != confirm_password:
                messages.warning(request, "Password didn't matched")
                return redirect("change-password")
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "password successfully changed")
                return redirect("profile", pk = user.id)
        return render(request, "booking/changePassword.html")
    else:
        messages.warning(request, "Login first")
        return redirect("login")