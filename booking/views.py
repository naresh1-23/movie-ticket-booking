from django.shortcuts import render

def home(request):
    return render(request, "booking/home.html")


def upcoming_movie(request, pk):
    return render(request, "booking/upcoming_movie.html")