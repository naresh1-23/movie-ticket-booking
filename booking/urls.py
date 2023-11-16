from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path("", views.home, name='home'),
    path("upcoming_movie/<int:pk>/", views.upcoming_movie, name = 'upcoming-movie'),
    path("tomorrow/", views.tomorrow, name = "tomorrow")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
