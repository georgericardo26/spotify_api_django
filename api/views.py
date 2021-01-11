import logging

from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import NotAuthenticated, NotFound
from rest_framework.response import Response
from rest_framework import status

from api.serializers import SearchInputSerializer, SearchAlbumOutputSerializer, PlaylistMeSerializer, \
    PlaylistTracksSerializer, SearchArtistOutputSerializer, ArtistTopTracksSerializer
from common.integrations.spotify.client import SpotifyWebAPIClient
from common.integrations.spotify.exception import ValidationError, UnauthorizedError

logger = logging.getLogger(__name__)


class SearchAlbumView(generics.ListAPIView):
    """
    View to search Albums
    """
    permission_classes = [permissions.AllowAny]

    logger.info("Initiating SearchAlbumView..", key="SearchAlbumView")

    def list(self, request, *args, **kwargs):
        params = request.query_params
        serializer = SearchInputSerializer(data=params)

        if serializer.is_valid():
            try:
                spotify_response = SpotifyWebAPIClient().search(query=params)
                serializer_albums = SearchAlbumOutputSerializer(data=spotify_response.get("albums"))
                serializer_albums.is_valid()
                return Response(data=serializer_albums.data, status=status.HTTP_200_OK)

            except ValidationError:
                raise serializers.ValidationError()

            except UnauthorizedError:
                raise NotAuthenticated()

            except NotFound:
                raise NotFound()

        response_data = {
            "code": "missing_query_parameters",
            "message": "One or more query parameter could not be validated."
        }

        return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)


class SearchArtistView(generics.ListAPIView):
    """
    View to search Artists
    """
    permission_classes = [permissions.AllowAny]

    logger.info("Initiating SearchAlbumView..", key="SearchAlbumView")

    def list(self, request, *args, **kwargs):
        params = request.query_params
        serializer = SearchInputSerializer(data=params)

        if serializer.is_valid():
            try:
                spotify = SpotifyWebAPIClient()
                spotify.check_token()
                response = spotify.search(query=params)

                serializer_artists = SearchArtistOutputSerializer(data=response.get("artists"))
                serializer_artists.is_valid()

                return Response(data=serializer_artists.data, status=status.HTTP_200_OK)

            except ValidationError:
                raise serializers.ValidationError()

            except UnauthorizedError:
                raise NotAuthenticated()

            except NotFound:
                raise NotFound()

            except Exception as e:
                raise Exception("Server error")

        response_data = {
            "code": "missing_query_parameters",
            "message": "One or more query parameter could not be validated."
        }

        return Response(data=response_data, status=status.HTTP_404_NOT_FOUND)


class PlaylistMeView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    logger.info("Initiating PlaylistMeView..", key="PlaylistMeView")

    def list(self, request, *args, **kwargs):
        params = request.query_params
        try:
            spotify = SpotifyWebAPIClient()
            spotify.check_token()
            response = spotify.playlist(query=params)
            serializer_playlists = PlaylistMeSerializer(data=response)
            serializer_playlists.is_valid()
            return Response(data=serializer_playlists.data, status=status.HTTP_200_OK)

        except ValidationError:
            raise serializers.ValidationError()

        except UnauthorizedError:
            raise NotAuthenticated()

        except NotFound:
            raise NotFound()


class PlaylistTracksView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    logger.info("Initiating PlaylistTracksView..", key="PlaylistTracksView")

    def list(self, request, *args, **kwargs):

        params = request.query_params
        playlist_id = kwargs.get("playlist_id")

        try:
            spotify = SpotifyWebAPIClient()
            spotify.check_token()
            response = spotify.playlist_tracks(query=params, parameter_route=playlist_id)
            serializer_playlist_tracks = PlaylistTracksSerializer(data=response)
            serializer_playlist_tracks.is_valid()
            return Response(data=serializer_playlist_tracks.data, status=status.HTTP_200_OK)

        except ValidationError:
            raise serializers.ValidationError()

        except UnauthorizedError:
            raise NotAuthenticated()

        except NotFound:
            raise NotFound()


class ArtistTopTracksView(generics.ListAPIView):

    permission_classes = [permissions.AllowAny]

    logger.info("Initiating ArtistTopTracksView..", key="ArtistTopTracksView")

    def list(self, request, *args, **kwargs):

        params = request.query_params
        artist_id = kwargs.get("artist_id")

        try:
            spotify = SpotifyWebAPIClient()
            spotify.check_token()
            response = spotify.top_tracks(query=params, parameter_route=artist_id)
            serializer_artist_tracks = ArtistTopTracksSerializer(data=response)
            serializer_artist_tracks.is_valid()
            return Response(data=serializer_artist_tracks.data, status=status.HTTP_200_OK)

        except ValidationError:
            raise serializers.ValidationError()

        except UnauthorizedError:
            raise NotAuthenticated()

        except NotFound:
            raise NotFound()