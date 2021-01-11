import logging
from urllib.parse import urljoin

from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
from rest_framework import serializers


logger = logging.getLogger(__name__)

local_request = HttpRequest()
local_request.META['SERVER_NAME'] = settings.SERVER_NAME
local_request.META['SERVER_PORT'] = settings.SERVER_PORT


class SearchInputSerializer(serializers.Serializer):
    q = serializers.CharField(required=True)
    type = serializers.CharField(required=True)


class AlbumsChildSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_tracks = serializers.IntegerField()
    type = serializers.CharField()


class UrlResultField(serializers.CharField):

    def to_internal_value(self, data):
        value = super(UrlResultField, self).to_internal_value(data)
        if value:
            try:
                query = value.split("?")[1]
                query = query.replace("query", "q")
                host = ":".join([local_request.META['SERVER_NAME'], local_request.META['SERVER_PORT']])
                url = "".join(["http://", host, "/api/spotify/search/albums/"])
                value = "?".join([url, query])

                return value

            except IndexError:
                return ""

        return value

    def to_representation(self, value):
        return str(value)


class UrlTrackResultField(serializers.CharField):

    def to_internal_value(self, data):
        value = super(UrlTrackResultField, self).to_internal_value(data)
        if value:
            try:
                query = value.split("playlists/")[1]
                query = query.split("/")[0]
                host = ":".join([local_request.META['SERVER_NAME'], local_request.META['SERVER_PORT']])
                url = "".join(["http://", host, "/api/spotify/playlists/{}/tracks/".format(query)])
                return value

            except IndexError:
                return ""

        return value

    def to_representation(self, value):
        return str(value)


class SearchAlbumOutputSerializer(serializers.Serializer):
    items = AlbumsChildSerializer(many=True, required=False)
    limit = serializers.IntegerField(required=False)
    next = UrlResultField(required=False, allow_null=True)
    offset = serializers.IntegerField(required=False)
    previous = UrlResultField(required=False, allow_null=True)
    total = serializers.IntegerField(required=False)


class ArtistChildSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    id = serializers.CharField(required=False)
    type = serializers.CharField(required=False)


class SearchArtistOutputSerializer(serializers.Serializer):
    items = ArtistChildSerializer(many=True, required=False)
    limit = serializers.IntegerField(required=False)
    next = UrlResultField(required=False, allow_null=True)
    offset = serializers.IntegerField(required=False)
    previous = UrlResultField(required=False, allow_null=True)
    total = serializers.IntegerField(required=False)


class TrackChildUrl(serializers.Serializer):
    href = UrlTrackResultField()
    total = serializers.IntegerField(required=False)


class PlaylistMeChild(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_null=True)
    tracks = TrackChildUrl()
    type = serializers.CharField(required=False, allow_null=True)


class PlaylistMeSerializer(serializers.Serializer):
    items = PlaylistMeChild(many=True, required=False)
    limit = serializers.IntegerField(required=False)
    next = UrlResultField(required=False, allow_null=True)
    offset = serializers.IntegerField(required=False)
    previous = UrlResultField(required=False, allow_null=True)
    total = serializers.IntegerField(required=False)


class UrlPlaylistField(serializers.CharField):

    def to_internal_value(self, data):
        value = super(UrlPlaylistField, self).to_internal_value(data)
        if value:
            try:
                query = value.split("?")[1]

                absolute_url = local_request.build_absolute_uri()
                absolute_url = urljoin(absolute_url, reverse("spotify:playlist_tracks"))
                value = "?".join([absolute_url, query])

                return value

            except IndexError:
                return ""

        return value

    def to_representation(self, value):
        return str(value)


class TrackChild(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()


class PlaylistTrackChild(serializers.Serializer):
    track = TrackChild(required=False)


class PlaylistTracksSerializer(serializers.Serializer):
    items = PlaylistTrackChild(many=True, required=False)
    limit = serializers.IntegerField(required=False)
    next = UrlResultField(required=False, allow_null=True)
    offset = serializers.IntegerField(required=False)
    previous = UrlResultField(required=False, allow_null=True)
    total = serializers.IntegerField(required=False)


class ArtistTopTracksSerializer(serializers.Serializer):
    tracks = TrackChild(many=True, required=False)
