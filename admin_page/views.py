from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Movie, NowShowing, ShowTime
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.
def now_showing(request):
    movies = NowShowing.objects.all()
    return render(request, "admin_page/show_now_showing_movie.html",{"movies": movies})

def add_movie(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        releasing_data = request.POST["releasing_date"]
        runtime = request.POST["runtime"]
        director = request.POST["director"]
        cast = request.POST["cast"]
        genre = request.POST["genre"]
        trailer= request.POST["trailer"]
        poster = request.FILES["poster"]
        if name=="" or description == "" or releasing_data == "" or runtime == "" or director == "" or cast == ""or trailer == "" or poster == "" or genre == "":
            messages.warning(request, "Fields cannot be empty")
            return redirect("add-movie")
        else:
            runtime_check = runtime.split()
            if runtime_check[1] =="Hours" and runtime_check[3] == "Min":
                movie = Movie.objects.create(movie_name=name, movie_description=description, runtime= runtime, director=director, genre=genre, cast = cast, releasing_date=releasing_data, trailer_iframe=trailer, movie_poster = poster)
                movie.save()
                messages.success(request, "Successfully added")
                return redirect("add-movie")
            else:
                messages.warning(request, "runtime format is not matched")
                return redirect("add-movie")
    return render(request, "admin_page/add_movie.html")

def upcoming_movie(request):
    movies = Movie.objects.filter(releasing_date__gt= datetime.now().date())
    return render(request, "admin_page/upcoming_movie.html", {"movies": movies})

def movies(request):
    movies = Movie.objects.all()
    return render(request, "admin_page/movies.html", {"movies": movies})

def add_now_showing(request, pk):
    movie = Movie.objects.filter(id = pk).first() 
    if request.method == "POST":
        time = request.POST["time"]
        date = request.POST["date"]
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
        show_time_check = ShowTime.objects.filter(time = time ,date = date).first()
        current_time_string = timezone.now().now().strftime("%H:%M %P")
        current_time = datetime.strptime(current_time_string, "%H:%M %p").time()
        selected_time = datetime.strptime(time, "%H:%M").time()
        print(current_time)
        print(selected_time)
        if date == "" or time == "":
            messages.warning(request, "Fields cannot be empty")
            return redirect("add-now-showing", pk = pk)
        if show_time_check:
            messages.warning(request, "There is already show at this time. Please select another time.")
            return redirect("add-now-showing", pk = pk)
        else:
            if movie.releasing_date > selected_date:
                messages.warning(request, "the movie is not yet to release")
                return redirect("add-now-showing", pk = pk)
            if current_time > selected_time and selected_date == datetime.now().date():
                messages.warning(request, "Please select appropriate time")
                return redirect("add-now-showing", pk = pk)
            else:
                now_showing_check = NowShowing.objects.filter(running_date=date,movie=movie).first()
                if now_showing_check:
                    show_time = ShowTime.objects.create(time = time, date = date)
                    show_time.save()
                    now_showing_check.show_time.add(show_time) 
                    now_showing_check.save()
                    messages.success(request, "Movie successfully added to now showing")
                    return redirect("now-showing")
                now_showing = NowShowing.objects.create(running_date=date, movie = movie)
                show_time = ShowTime.objects.create(time = time, date = date)
                show_time.save()
                now_showing.show_time.add(show_time)
                now_showing.save()
                messages.success(request, "Movie successfully added to now showing")
                return redirect("now-showing")
    return render(request, "admin_page/add_now_showing.html", {"movie": movie})


def delete_movie(request, pk):
    movie = Movie.objects.filter(id = pk).first()
    movie.delete()
    return redirect("movies")


def delete_now_showing_movie(request, pk):
    movies = NowShowing.objects.filter(movie = pk)
    movies.delete()
    return redirect("now-showing")