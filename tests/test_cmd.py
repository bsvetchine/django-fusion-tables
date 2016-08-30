from distutils.core import Command


class TestCommand(Command):
    description = "Launch all tests under fusion_tables app"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

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
        self.configure_settings()
        django.setup()
        call_command("test", "fusion_tables")
