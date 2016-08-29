"""Google server to server authentication through service account."""
from httplib2 import Http

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from . import app_settings


def get_service():
    scopes = ["https://www.googleapis.com/auth/fusiontables"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        app_settings.CLIENT_SECRET_JSON_FILEPATH, scopes=scopes)
    if app_settings.DELEGATED_CREDENTIALS:
        credentials = credentials.create_delegated(
            app_settings.DELEGATED_CREDENTIALS)
    http_auth = credentials.authorize(Http())
    return build('fusiontables', 'v2', http=http_auth)
