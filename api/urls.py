from django.contrib import admin
from django.urls import path, include

from api import views

app_name = "spotify"

urlpatterns = [
    path('search/albums/', views.SearchAlbumView.as_view(), name='search_album'),
    path('search/artists/', views.SearchArtistView.as_view(), name='search_artist'),
    path('playlists/me/', views.PlaylistMeView.as_view(), name='my_playlist'),
    path('playlists/<slug:playlist_id>/tracks/', views.PlaylistTracksView.as_view(), name='playlist_tracks'),
    path('artists/<slug:artist_id>/top-tracks/', views.ArtistTopTracksView.as_view(), name='artist_top_tracks'),
]
