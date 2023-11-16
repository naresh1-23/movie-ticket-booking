from django.shortcuts import render
from admin_page.models import Movie, NowShowing
from datetime import datetime, timedelta
from django.db.models import Count
import json
from django.http import HttpResponse


def home(request):
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