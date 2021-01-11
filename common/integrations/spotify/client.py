import urllib
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache
from rest_framework import status

from common.integrations.spotify.exception import handle_error_response
from common.integrations.spotify.session import SpotifyAPISession


class SpotifyAPIBaseClient(object):

    def __init__(self):
        """
        Instantiate a new API client.
        """

        # Initialize the session.
        self.session = SpotifyAPISession()

    # Convenience method for building request URLs.
    @property
    def url(self):
        return urljoin(self.host, self.version)

    # Perform an API request.
    def _request(self, method, endpoint, params=None, data=None):

        url = urljoin(self.url, endpoint)

        if params:
            params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

        resp = self.session.request(method, url, params=params, data=data, headers=self.session.headers)

        # # If something goes wrong, we'll pass the response
        # # off to the error-handling code
        if resp.status_code >= status.HTTP_400_BAD_REQUEST:
            handle_error_response(resp)

        # Otherwise return the result dictionary.
        return resp.json()


class SpotifyAuthenticationAPIClient(SpotifyAPIBaseClient):

    def __init__(self):
        super(SpotifyAuthenticationAPIClient, self).__init__()
        self.version = ""
        self.host = settings.SPOTIFY_URL_AUTH

    def _get_token_data(self):
        return dict(
            grant_type="client_credentials",
            scopes="playlist-read-private, playlist-modify-public, playlist-modify-private, playlist-read-collaborative, user-read-private, user-read-email"
        )

    # API methods
    def auth(self, client_id, secret_id):
        self.session.init_basic_auth(client_id, secret_id)
        return self._request("POST", "token", data=self._get_token_data())


class SpotifyWebAPIClient(SpotifyAPIBaseClient):
    
    def __init__(self):
        super(SpotifyWebAPIClient, self).__init__()
        self.version = settings.SPOTIFY_VERSION
        self.host = settings.SPOTIFY_URL_WEB_API

    def check_token(self):
        if not cache.get("api_token"):
            auth = SpotifyAuthenticationAPIClient()
            response = auth.auth(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_SECRET_ID)
            cache.set("api_token", response.get("access_token"), response.get("expires_in"))

    def search(self, query):
        # Check if token has been expired
        self.check_token()
        self.session.init_barer_auth(cache.get("api_token"))
        return self._request('GET', 'search', params=query)

    def playlist(self, query):

        self.session.init_barer_auth(cache.get("api_token"))
        return self._request('GET', 'users/{}/playlists'.format(settings.SPOTIFY_USER_ID), params=query)

    def top_tracks(self, query, parameter_route):
        self.session.init_barer_auth(cache.get("api_token"))
        return self._request('GET', 'artists/{}/top-tracks'.format(parameter_route), params=query)

    def playlist_tracks(self, query, parameter_route):
        self.session.init_barer_auth(cache.get("api_token"))
        return self._request('GET', 'playlists/{}/tracks'.format(parameter_route), params=query)
