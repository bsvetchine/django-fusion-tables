from django.conf import settings


CLIENT_SECRET_JSON_FILEPATH = getattr(settings, "CLIENT_SECRET_JSON_FILEPATH")
DELEGATED_CREDENTIALS = getattr(settings, "DELEGATED_CREDENTIALS", "")
