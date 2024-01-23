from django.contrib import admin
from .models import Movie, NowShowing, ShowTime, Booked
from django.contrib.admin import register, ModelAdmin


@register(Movie)
class MovieAdmin(ModelAdmin):
    list_display=("movie_name", "director", "genre", "releasing_date")
    
@register(NowShowing)
class NowSHowingAdmin(ModelAdmin):
    list_display = ("movie", 'running_date')
    
    
@register(ShowTime)
class ShowtimeAdmin(ModelAdmin):
    list_display = ("time", 'date')
    
@register(Booked)
class BookedAdmin(ModelAdmin):
    list_display = ("user", "seat", "show", "time")

# Register your models here.
