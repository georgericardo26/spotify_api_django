from django.contrib import admin
from django.urls import path, include

from web import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('albums/', views.SearchAlbumView.as_view()),
    path('toptracks/', views.TopTracksView.as_view()),
]
