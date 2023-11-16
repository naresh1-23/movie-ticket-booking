from django.contrib import admin
from .models import Movie, NowShowing, ShowTime


admin.site.register(Movie)
admin.site.register(NowShowing)
admin.site.register(ShowTime)
# Register your models here.
