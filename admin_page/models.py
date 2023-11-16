from django.db import models

class Movie(models.Model):
    movie_name = models.CharField(max_length=250)
    movie_poster = models.FileField(upload_to="movie/")
    movie_description = models.TextField()
    releasing_date = models.DateField()
    director = models.CharField(max_length=250)
    runtime = models.CharField(max_length=100)
    genre = models.TextField()
    cast = models.TextField()
    trailer_iframe = models.TextField()
    
    def __str__(self):
        return self.movie_name

class ShowTime(models.Model):
    time = models.TimeField()
    date = models.DateField()
    
    def __str__(self):
        return f"movie_time {self.time} at "
    


class NowShowing(models.Model):
    show_time = models.ManyToManyField("ShowTime")
    running_date = models.DateField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.movie.movie_name} in {self.running_date} at {self.show_time}"
    
  