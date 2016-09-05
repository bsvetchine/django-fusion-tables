import os

from distutils.core import Command

from django.template.loader import render_to_string


ROOT = os.path.dirname(__file__)


class TestCommand(Command):
    description = "Launch all tests under fusion_tables app"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def generate_client_secret():
        client_secret_json_tpl = os.path.join(ROOT, "client_secret.json")
        client_secret = render_to_string(client_secret_json_tpl, {
            "project_id": os.environ.get("PROJECT_ID"),
            "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
            "private_key": os.environ.get("PRIVATE_KEY"),
            "client_email": os.environ.get("CLIENT_EMAIL"),
            "client_id": os.environ.get("CLIENT_ID"),
            "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL")
        })
        client_secret_file = open("/tmp/client_secret.json", "w")
        client_secret.file.write(client_secret)
        client_secret_file.close()

    def configure_settings(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                "default": {
                    "NAME": ":memory:",
                    "ENGINE": "django.db.backends.sqlite3",
                    "TEST": {
                        "NAME": ":memory:"
                    }
                }
            },
            INSTALLED_APPS=(
                "django.contrib.contenttypes",
                "fusion_tables",
            ),
            ROOT_URLCONF="tests.urls",
            MODELS_TO_SYNC=("fusion_tables.SampleModel", ),
            CLIENT_SECRET_JSON_FILEPATH="/tmp/client_secret.json",
            LOCATION_FIELDS=("TextField", )
        )

    def run(self):
        import django
        from django.core.management import call_command
        self.generate_client_secret()
        self.configure_settings()
        django.setup()
        call_command("test", "fusion_tables")
