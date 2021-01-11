import requests
from urllib.parse import urljoin

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView

# from .forms import MyForm
from api import views as api_views


class HomeView(TemplateView):
    template_name = "home.html"


class SearchAlbumView(View):
    template_name = 'search_albums.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        field_value = request.POST.get("search_name")

        host = request.META['HTTP_HOST']
        url = "".join(["http://", host, "/api/spotify/search/albums/"])
        response = requests.get(url=url, params={"q": field_value, "type": "album"})

        data_context = {
            "data": response.json()
        }

        return render(request, self.template_name, data_context)

class TopTracksView(View):
    template_name = 'top_tracks.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        field_artist = request.POST.get("artist_name")
        field_market = request.POST.get("market")
        host = request.META['HTTP_HOST']

        artist = self.get_artist_id(request, field_artist, host)
        artist = artist["items"][0]
        top_tracks = self.get_top_tracks(request, artist["id"], field_market, host)

        my_playlist_id = self.get_my_playlist(request, host)
        tracks = self.get_my_tracks(request, host, my_playlist_id)

        data_context = {
            "artist_name": artist["name"],
            "top_tracks": top_tracks,
            "my_tracks": tracks
        }

        return render(request, self.template_name, data_context)

    def get_my_playlist(self, request, host):
        url = "".join(["http://", host, "/api/spotify/playlists/me/"])
        response = requests.get(url=url).json()
        response = response["items"][0]["id"]
        return response

    def get_my_tracks(self, request, host, my_playlist_id):
        url = "".join(["http://", host, "/api/spotify/playlists/{}/tracks/".format(my_playlist_id)])
        response = requests.get(url=url).json()
        name_list = [obj["track"]["name"] for obj in response["items"]]
        return name_list

    def get_artist_id(self, request, artist, host):
        url = "".join(["http://", host, "/api/spotify/search/artists/"])
        response = requests.get(url=url, params={"q": artist, "type": "artist"}).json()
        return response

    def get_top_tracks(self, request, artist_id, field_market, host):
        url = "".join(["http://", host, "/api/spotify/artists/{}/top-tracks/".format(artist_id)])
        response = requests.get(url=url, params={"market": field_market}).json()
        return response["tracks"]

    def make_request(self, params=None, lookup=None):
        pass