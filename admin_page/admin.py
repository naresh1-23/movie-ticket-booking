from django.contrib import admin
from .models import Movie, NowShowing, ShowTime
from django.contrib.admin import register, ModelAdmin


@register(Movie)
class MovieAdmin(ModelAdmin):
    list_display=("movie_name", "director", "genre", "releasing_date")
    icon_name  = 'movie'
    
@register(NowShowing)
class NowSHowingAdmin(ModelAdmin):
    list_display = ("movie", 'running_date')
    icon_name = 'slideshow'
    
    
@register(ShowTime)
class ShowtimeAdmin(ModelAdmin):
    list_display = ("time", 'date')
    icon_name = 'timer'
# Register your models here.
