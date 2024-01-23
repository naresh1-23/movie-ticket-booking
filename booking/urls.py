from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path("", views.home, name='home'),
    path("upcoming_movie/<int:pk>/", views.upcoming_movie, name = 'upcoming-movie'),
    path("tomorrow/", views.tomorrow, name = "tomorrow"),
    path("seat_booking/<int:pk>/<str:tom>/<str:showtime>/", views.seat_booking, name = 'seat-booking'),
    path("profile/<int:pk>/", views.profile, name = "profile"),
    path("edit-profile/<int:pk>/", views.editProfile, name = "editprofile"),
    path("changePassword/", views.changePassword, name = "change-password")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
