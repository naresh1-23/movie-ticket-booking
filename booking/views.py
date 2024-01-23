from django.shortcuts import render, redirect
from admin_page.models import Movie, NowShowing, ShowTime, Booked
from datetime import datetime, timedelta
from django.db.models import Count
import json
from django.http import HttpResponse
from django.contrib import messages


def home(request):
    delete_movie = NowShowing.objects.filter(running_date__lt = datetime.now().date())
    delete_movie.delete()
    delete_showtime = ShowTime.objects.filter(date__lt = datetime.now().date())
    delete_showtime.delete()
    movies = Movie.objects.filter(releasing_date__gt = datetime.now().date())
    now_showing_movies = NowShowing.objects.filter(running_date=datetime.now().date())
    tom = False
    return render(request, "booking/home.html", {"movies": movies, "now_showing_movies": now_showing_movies, "tom": tom})


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
    seat_range = [1,2,3,4,5,6,7,8]
    return render(request,"booking/seat_booking.html", {'movie': movie, "now_showing_movies": now_showing_movies,"tomm": tomm, "seat_range": seat_range , "showtime_obj": showtime_obj.time})


