from base64 import b64encode
from requests import Session


class SpotifyAPISession(Session):

    def __init__(self, *args, **kwargs):
        super(SpotifyAPISession, self).__init__()

        self.headers.update({
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/x-www-form-urlencoded'
        })

    def init_basic_auth(self, client_id, secret_id):
        credentials = b64encode('{}:{}'.format(client_id, secret_id).encode())
        self.headers.update({
            'Authorization': 'Basic {}'.format(credentials.decode())
        })

    def init_barer_auth(self, token):
        self.headers.update({
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'application/json'
        })
