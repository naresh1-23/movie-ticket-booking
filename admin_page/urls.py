from django.urls import path
from . import views


urlpatterns = [
    path("now_showing/", views.now_showing, name="now-showing"),
    path("add_movie/", views.add_movie, name = "add-movie"),
    path("upcoming_movies/", views.upcoming_movie, name = 'upcoming-movie'),
    path("add_now_showing/<int:pk>/", views.add_now_showing, name = 'add-now-showing'),
    path("movies/", views.movies, name = "movies"),
    path("delete_movies/<int:pk>/", views.delete_movie, name = "delete-movie"),
    path("delete_now_showing/<int:pk>/", views.delete_now_showing_movie, name = "delete-now-showing"),
]
